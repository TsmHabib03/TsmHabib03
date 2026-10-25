"""Hero contracts: deterministic assets, fallbacks and complete train exit."""
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
                ET.fromstring(source)
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

    def test_motion_uses_train_geometry_and_holds_after_exit(self):
        for mobile, width in ((False, 1200), (True, 600)):
            source = profile.hero(mobile=mobile)
            start, end, _ = city.train_positions(width)
            self.assertIn(f"translateX({start}px)", source)
            self.assertIn(f"{city.TRAIN_TRAVEL_PERCENT}%,100% {{ transform:translateX({end}px)", source)
            self.assertIn("prefers-reduced-motion:reduce", source)
            still = profile.hero(mobile=mobile, animated=False)
            self.assertNotIn("<style>", still)
            self.assertNotIn("@keyframes", still)
            self.assertEqual(still.count('class="carriage"'), 3)

    def test_bitmap_name_and_label_fit_each_layout(self):
        for value, cell, width in ((profile.NAME, 10, 1200), ("HABIB", 9, 600), ("JAUDIAN D.", 9, 600), ("TOKYO AFTER HOURS", 3, 600)):
            self.assertLessEqual(32 + profile.pixel_width(value, cell), width - 32)

    def test_readme_structure_and_asset_references(self):
        source = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^## (.+)$", source, re.M), ["About Me", "Current Focus", "Tech Stack", "Connect"])
        self.assertNotIn("project-", source)
        for path in re.findall(r'(?:src|srcset)="([^"]+)"', source):
            self.assertTrue((ROOT / path).is_file(), path)
        self.assertIn("hero-mobile-still.svg", source)
        self.assertIn("hero-still.svg", source)


if __name__ == "__main__":
    unittest.main()
