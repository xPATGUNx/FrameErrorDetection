import unittest
import FrameDetector


class TestFrameDropDetection(unittest.TestCase):
    def test_videos_for_frame_drops(self):
        video = 'Elgato/60 FPS.mp4'
        detected_frame_drops = FrameDetector.frame_drop_detection(video, 150)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))


if __name__ == '__main__':
    unittest.main()
