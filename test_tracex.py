import unittest
from src.tracex import make_frame, TOTAL_FRAMES, W, H

class TestTraceX(unittest.TestCase):
    def test_video_duration_frames(self):
        self.assertEqual(TOTAL_FRAMES, 36 * 24)

    def test_frame_dimensions(self):
        frame = make_frame(0)
        self.assertEqual(frame.size, (W, H))
        self.assertEqual(frame.mode, 'RGB')

if __name__ == '__main__':
    unittest.main()
