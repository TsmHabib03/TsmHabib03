"""Verify bounded motion and readable stationary content after GIF delivery."""
from pathlib import Path
import unittest

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class FooterDelivery(unittest.TestCase):
    def test_motion_is_bounded_to_the_edge_and_finishes_at_rest(self):
        for suffix, size in (('', (1200, 240)), ('-mobile', (600, 320))):
            with self.subTest(suffix=suffix), Image.open(ROOT / f'assets/readme/connect-banner{suffix}.gif') as gif:
                self.assertEqual(gif.size, size)
                self.assertNotIn('loop', gif.info)
                self.assertIn(b'Gruppo', gif.info['comment'])
                self.assertLess(Path(gif.filename).stat().st_size, 1_000_000)
                first = np.array(gif.convert('RGB'))
                duration = 0
                moving_pixels = 0
                for index in range(gif.n_frames):
                    gif.seek(index)
                    duration += gif.info['duration']
                    pixels = np.array(gif.convert('RGB'))
                    self.assertTrue(np.array_equal(first[96:], pixels[96:]), 'Text or social icons moved')
                    moving_pixels = max(moving_pixels, int(np.count_nonzero(first[:96] != pixels[:96])))
                self.assertEqual(duration, 3000)
                self.assertGreater(moving_pixels, 100)
                self.assertTrue(np.array_equal(first, np.array(gif.convert('RGB'))), 'Ripple did not settle')
                with Image.open(ROOT / f'assets/readme/connect-banner{suffix}-still.png') as still:
                    self.assertEqual(still.size, size)
                    self.assertIn('Gruppo', still.info['Description'])
                    self.assertTrue(np.array_equal(first[:96], np.array(still)[:96]))


if __name__ == '__main__':
    unittest.main()
