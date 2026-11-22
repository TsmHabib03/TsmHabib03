"""Check the shipped motion, loop, and stationary identity in the README GIFs."""
from pathlib import Path
import importlib.util
import unittest

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("globe",ROOT/"scripts/build-globe-banner.py")
globe=importlib.util.module_from_spec(spec)
spec.loader.exec_module(globe)


class GlobeDelivery(unittest.TestCase):
    def test_motion_and_identity_survive_gif_encoding(self):
        for mobile in (False,True):
            name="profile-globe"+("-mobile" if mobile else "")
            with self.subTest(mobile=mobile), Image.open(ROOT/f"assets/readme/{name}.gif") as im:
                self.assertEqual(im.size,globe.layout(mobile)[0])
                self.assertEqual(im.n_frames,150)
                self.assertEqual(im.info["loop"],0)
                self.assertIn(b"Natural Earth",im.info["comment"])
                self.assertLess((ROOT/f"assets/readme/{name}.gif").stat().st_size,8_000_000)
                first=np.array(im.convert("RGB"))
                self.assertEqual(tuple(first[0,0]), (255,255,255))
                blue_pixel = first[310,0] if mobile else first[0,700]
                self.assertEqual(tuple(blue_pixel), globe.BLUE)
                total=0
                for index in range(im.n_frames):
                    im.seek(index)
                    total+=im.info["duration"]
                self.assertEqual(total,10000)
                last=np.array(im.convert("RGB"))
                im.seek(75)
                middle=np.array(im.convert("RGB"))
                identity=(slice(0,300),slice(None)) if mobile else (slice(None),slice(0,670))
                self.assertTrue(np.array_equal(first[identity],middle[identity]))
                self.assertTrue(np.array_equal(first[identity],last[identity]))
                self.assertGreater(np.mean(np.abs(first.astype(float)-middle.astype(float))),1)
                # A wrap step must resemble adjacent frames, not a teleport.
                seam=np.mean(np.abs(first.astype(float)-last.astype(float)))
                im.seek(1)
                adjacent=np.mean(np.abs(first.astype(float)-np.array(im.convert("RGB")).astype(float)))
                self.assertLess(seam,adjacent*1.8)

    def test_rotation_is_periodic_and_stills_have_provenance(self):
        self.assertTrue(np.array_equal(np.array(globe.frame(0)),np.array(globe.frame(150))))
        for suffix in ("","-mobile"):
            with Image.open(ROOT/f"assets/readme/profile-globe{suffix}-still.png") as im:
                self.assertIn("Natural Earth",im.info["Description"])


if __name__=="__main__":
    unittest.main()
