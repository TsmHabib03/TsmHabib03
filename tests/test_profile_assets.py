"""Current README references and retained deterministic artwork contracts."""
import importlib.util
from pathlib import Path
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
        self.assertEqual(re.findall(r"<h2><samp>(.+?)</samp></h2>", source), [
            "About", "Tech Stack", "Education", "Connection"])
        self.assertNotRegex(source, r"assets/(?:hero|section-|project-|pixel-cat)|<style|\sstyle=|<script")
        for path in re.findall(r'(?:src|srcset)="([^"]+)"', source):
            if path.startswith("https://"):
                self.assertTrue(path.startswith("https://img.shields.io/badge/"), path)
            else:
                self.assertTrue((ROOT / path).is_file(), path)
        self.assertNotRegex(source, r'Featured Work|FEATURED WORK|night-city-cat|github\.io|placeholder|profile\.html')
        self.assertEqual(source.count('<table>'), 1)
        stack = source.split('<samp>Tech Stack</samp>')[1].split('<samp>Education</samp>')[0]
        self.assertEqual(re.findall(r"<h3>(.+?)</h3>", stack), ["Frontend", "Backend", "Database", "Tools"])
        self.assertEqual(re.findall(r'alt="([^"]+)"', stack), [
            "HTML", "CSS", "JavaScript", "Tailwind CSS", "Bootstrap", "PHP", "Java",
            "MySQL", "Git", "GitHub", "Docker", "VS Code",
        ])
        contact = source.split('<samp>Connection</samp>')[1]
        self.assertEqual(contact.count('width="32" height="32"'), 4)
        self.assertIn('https://www.facebook.com/habib.jaudian.1', contact)
        self.assertIn('https://www.instagram.com/tsmhabib03', contact)
        self.assertLess(contact.index('connect-banner.svg'), contact.index('assets/marks/facebook.svg'))

    def test_retained_profile_assets_are_self_contained(self):
        outputs = profile.profile_assets()
        self.assertEqual(outputs, profile.profile_assets())
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        references = set(re.findall(r'(?:src|srcset)="assets/([^"]+)"', readme))
        self.assertEqual(references, {"readme/profile-banner.svg", "readme/profile-banner-mobile.svg",
                                      "readme/connect-banner.svg", "readme/connect-banner-mobile.svg",
                                      "marks/facebook.svg", "marks/instagram.svg", "marks/github.svg", "marks/email.svg"})
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
