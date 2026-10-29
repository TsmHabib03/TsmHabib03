"""Current README references and retained deterministic artwork contracts."""
import importlib.util
from pathlib import Path
from html import unescape
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("profile_assets", ROOT / "scripts/generate-profile-assets.py")
profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profile)
import pixel_city as city
stack_spec = importlib.util.spec_from_file_location("readme_stack", ROOT / "scripts/build-readme-stack.py")
stack_assets = importlib.util.module_from_spec(stack_spec)
stack_spec.loader.exec_module(stack_assets)


class HeroContracts(unittest.TestCase):
    def test_shipped_heroes_match_deterministic_generation(self):
        outputs = profile.generate_assets(hero_only=True)
        self.assertEqual(set(outputs), {"hero.svg", "hero-still.svg", "hero-mobile.svg", "hero-mobile-still.svg"})
        self.assertEqual(outputs, profile.generate_assets(hero_only=True))
        for name, source in outputs.items():
            with self.subTest(asset=name):
                root = ET.fromstring(source)
                ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
                references = re.findall(r'url\(#([^\)]+)\)|href="#([^"]+)"', source)
                for url_id, href_id in references:
                    self.assertIn(url_id or href_id, ids)
                self.assertEqual(source, (ROOT / "assets" / name).read_text(encoding="utf-8"))
                self.assertNotRegex(source, r"<(?:script|filter|image|linearGradient|radialGradient)\b")

    def test_train_and_fallback_fit_the_scene(self):
        for width in (600, 1200):
            start, end, still = city.train_positions(width)
            self.assertLessEqual(start + city.TRAIN_WIDTH, -city.TRAIN_MARGIN)
            self.assertGreaterEqual(end, width + city.TRAIN_MARGIN)
            self.assertGreaterEqual(still, city.TRAIN_MARGIN)
            self.assertLessEqual(still + city.TRAIN_WIDTH, width - city.TRAIN_MARGIN)
        self.assertEqual(city.commuter_train().count('class="carriage"'), 3)

    def test_current_scenes_only_animate_tail_and_sparse_windows(self):
        for mobile in (False, True):
            source = profile.hero(mobile=mobile)
            self.assertNotIn("train", source)
            self.assertNotIn("translateX", source)
            self.assertEqual(len(re.findall(r"@keyframes", source)), 5)
            self.assertIn("prefers-reduced-motion:reduce", source)
            still = profile.hero(mobile=mobile, animated=False)
            self.assertNotIn("<style>", still)
            self.assertNotIn("@keyframes", still)
            self.assertIn('class="night-cat" data-coat="calico"', still)

    def test_bitmap_name_and_label_fit_each_layout(self):
        for value, cell, width in ((profile.NAME, 10, 1200), ("HABIB", 9, 600), ("JAUDIAN D.", 9, 600), (profile.IDENTITY, 4, 600)):
            self.assertLessEqual(32 + profile.pixel_width(value, cell), width - 32)

    def test_readme_structure_and_asset_references(self):
        source = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"<h2>(.+?)</h2>", source), [
            "About", "Tech Stack", "Education", "Connection"])
        self.assertNotRegex(source, r"assets/(?:hero|section-|project-|pixel-cat)|<style|\sstyle=|<script")
        for path in re.findall(r'(?:src|srcset)="([^"]+)"', source):
            if path.startswith("https://"):
                self.assertTrue(path.startswith("https://img.shields.io/badge/"), path)
            else:
                self.assertTrue((ROOT / path).is_file(), path)
        self.assertNotRegex(source, r'Featured Work|FEATURED WORK|night-city-cat|github\.io|placeholder|profile\.html')
        self.assertNotIn('<table', source)
        self.assertNotIn('<samp>', source)
        plain = unescape(re.sub(r'<[^>]+>', '', source))
        self.assertIn("I'm a BSCS student at Quezon City University who enjoys building web applications and exploring software engineering.", plain)
        self.assertIn('<h3>Building useful software, one project at a time.</h3>', source)
        self.assertEqual(source.count('<strong><ins>Quezon City University</ins></strong>'), 2)
        stack = source.split('<h2>Tech Stack</h2>')[1].split('<h2>Education</h2>')[0]
        self.assertNotIn('<h3>', stack)
        self.assertEqual(stack.count('<p>'), 1)
        self.assertEqual(re.findall(r'<img src="assets/readme/tech-[^>]+alt="([^"]+)"', stack), [
            "HTML", "CSS", "JavaScript", "Tailwind CSS", "Bootstrap", "PHP", "Java",
            "MySQL", "Git", "GitHub", "Docker", "VS Code",
        ])
        education = source.split('<h2>Education</h2>')[1].split('<h2>Connection</h2>')[0]
        self.assertEqual(re.findall(r'<h3><img[^>]+alt="([^"]+)"', education),
                         ["BS Computer Science", "NC III — Web Development"])
        self.assertIn('<h3><strong><ins>Quezon City University</ins></strong></h3>', education)
        self.assertIn('<h3><strong><ins>TESDA</ins></strong></h3>', education)
        contact = source.split('<h2>Connection</h2>')[1]
        self.assertEqual(contact.count('<a href='), 4)
        self.assertEqual(contact.count('<picture>'), 1)
        self.assertEqual(contact.count('<img '), 1)
        self.assertIn('<p align="center">', contact)
        self.assertIn('https://www.facebook.com/habib.jaudian.1', contact)
        self.assertIn('https://www.instagram.com/tsmhabib03', contact)
        self.assertLess(contact.index('connect-banner.svg'), contact.index('<a href='))
        self.assertIn('mailto:jaudianhabib879@gmail.com', contact)

    def test_retained_profile_assets_are_self_contained(self):
        outputs = profile.profile_assets()
        self.assertEqual(outputs, profile.profile_assets())
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        references = set(re.findall(r'(?:src|srcset)="assets/([^"]+)"', readme))
        self.assertEqual(references, {"readme/profile-banner.svg", "readme/profile-banner-mobile.svg",
                                      "readme/connect-banner.svg", "readme/connect-banner-mobile.svg"}
                         | {f"readme/{name}" for name in stack_assets.assets() if not name.startswith('heading-')})
        for name, source in stack_assets.assets().items():
            with self.subTest(readme_asset=name):
                root = ET.fromstring(source)
                self.assertEqual(source, (ROOT / "assets/readme" / name).read_text(encoding="utf-8"))
                self.assertNotRegex(source, r'<(?:script|filter|image|text|style)\b|https?://(?!www.w3.org)')
                self.assertNotIn('crispEdges', source)
                ids = {element.attrib['id'] for element in root.iter() if 'id' in element.attrib}
                for url_id, href_id in re.findall(r'url\(#([^\)]+)\)|href="#([^"]+)"', source):
                    self.assertIn(url_id or href_id, ids)
                if name.startswith('tech-'):
                    logo = root.find('{http://www.w3.org/2000/svg}use')
                    self.assertEqual((logo.attrib['width'], logo.attrib['height']), ('48', '48'))
                if name.startswith('education-'):
                    self.assertEqual(root.attrib['viewBox'], '0 0 288 64')
        for name, source in outputs.items():
            with self.subTest(asset=name):
                root = ET.fromstring(source)
                ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
                references = re.findall(r'url\(#([^\)]+)\)|href="#([^"]+)"', source)
                for url_id, href_id in references:
                    self.assertIn(url_id or href_id, ids)
                self.assertEqual(source, (ROOT / "assets" / name).read_text(encoding="utf-8"))
                self.assertNotRegex(source, r"<(?:script|filter|image|linearGradient|radialGradient)\b")
        self.assertNotRegex(readme, r"(?:tel:|\+63\d|\b09\d{9}\b)")

    def test_reference_banners_have_portable_type_and_static_motion_path(self):
        for name, source in stack_assets.banners.assets().items():
            with self.subTest(asset=name):
                ET.fromstring(source)
                self.assertEqual(source, (ROOT/'assets/readme'/name).read_text(encoding='utf-8'))
                self.assertNotRegex(source, r'<(?:script|image|text|a)\b|Silkscreen|crispEdges')
                self.assertIn('Open Sans', source)
                if name.startswith('profile-banner'):
                    self.assertIn('prefers-reduced-motion:reduce', source)
                    self.assertEqual(source.count('class="variation '), 3)
                    self.assertIn('18s ease-in-out infinite', source)
                    self.assertIn('class="variation orange" opacity="1"', source)
                if name.startswith('connect-') and 'banner' not in name:
                    self.assertEqual(len(re.findall(r'aria-label=', source)), 1)
                if name.startswith('connect-banner'):
                    for label in ('Facebook', 'Instagram', 'GitHub', 'Email'):
                        self.assertIn(f'aria-label="{label}"', source)

    def test_cat_motion_has_a_complete_static_alternative(self):
        for section in (None, *city.PROFILE_SECTIONS):
            for mobile in (False, True):
                with self.subTest(section=section, mobile=mobile):
                    render = profile.hero if section is None else lambda **kw: profile.section_banner(section, **kw)
                    animated = render(mobile=mobile)
                    still = render(mobile=mobile, animated=False)
                    self.assertIn(".cat-tail-pose,.flicker-window { animation:none }", animated)
                    self.assertIn('class="night-cat"', still)
                    self.assertIn('class="cat-tail-pose tail-rest" visibility="visible"', still)
                    cats = 1 if section is None else 3
                    self.assertEqual(still.count('class="night-cat"'),cats)
                    self.assertEqual(still.count('visibility="hidden"'), 3*cats)
                    self.assertNotIn("@keyframes", still)

    def test_each_section_has_four_variants_and_correct_dimensions(self):
        outputs = profile.profile_assets()
        self.assertEqual(len(outputs), 28)
        for section in city.PROFILE_SECTIONS:
            for mobile in (False, True):
                for still in (False, True):
                    suffix = ("-mobile" if mobile else "") + ("-still" if still else "")
                    root = ET.fromstring(outputs[f"section-{section}{suffix}.svg"])
                    self.assertEqual(root.attrib['viewBox'], f"0 0 {600 if mobile else 1200} 200")

    def test_coats_and_rooftops_match_the_two_scene_roles(self):
        for mobile in (False,True):
            hero = ET.fromstring(profile.hero(mobile=mobile))
            connect = ET.fromstring(profile.section_banner('connect',mobile=mobile))
            ns = {'s':'http://www.w3.org/2000/svg'}
            self.assertEqual([g.attrib['data-coat'] for g in hero.findall('.//s:g[@class="night-cat"]',ns)],['calico'])
            self.assertEqual([g.attrib['data-coat'] for g in connect.findall('.//s:g[@class="night-cat"]',ns)],['black','orange','calico'])
            for scene in (hero,connect):
                self.assertEqual(len(scene.findall('.//s:g[@class="cat-rooftop"]',ns)),1)
            for color in (city.CAT_COATS['calico']['base'],city.CAT_COATS['calico']['patch'],city.CAT_COATS['calico']['dark']):
                self.assertIn(color,profile.hero(mobile=mobile))

    def test_every_tail_pose_is_a_connected_pixel_silhouette(self):
        for coat in city.CAT_COATS:
            with self.subTest(coat=coat):
                self.assert_connected_tail(coat)

    def assert_connected_tail(self, coat):
        root = ET.fromstring('<svg>'+city.night_cat(100, 180, coat=coat)+'</svg>')
        for pose in root.iter('g'):
            if 'cat-tail-pose' not in pose.attrib.get('class', ''):
                continue
            path = next(p for p in pose if p.attrib.get('fill')==city.CAT_COATS[coat]['base'])
            boxes = [(int(x),int(y),int(w),int(h)) for x,y,w,h in
                     re.findall(r'M(-?\d+) (-?\d+)h(\d+)v(\d+)h-\d+z', path.attrib['d'])]
            self.assertTrue(boxes)
            # Edge contact is connected; diagonal point contact is insufficient.
            def touching(a, b):
                x,y,w,h = a
                bx,by,bw,bh = b
                dx = min(x+w,bx+bw)-max(x,bx)
                dy = min(y+h,by+bh)-max(y,by)
                return dx>=0 and dy>=0 and (dx>0 or dy>0)
            reached, pending = {0}, [0]
            while pending:
                current = pending.pop()
                for i, box in enumerate(boxes):
                    if i not in reached and touching(boxes[current],box):
                        reached.add(i)
                        pending.append(i)
            self.assertEqual(len(reached),len(boxes),pose.attrib['class'])


if __name__ == "__main__":
    unittest.main()
