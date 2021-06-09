import unittest
from FrameDetector import FrameDetector


class TestFrameDropDetection(unittest.TestCase):
    def test_videos_for_frame_drops(self):
        video = 'Video/Elgato/60 FPS.mp4'
        expected_video_frames = 150
        frame_detector = FrameDetector()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_drop_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_mkv_video_for_frame_drops(self):
        video = 'Video/Elgato/60 FPS.mkv'
        expected_video_frames = 150
        frame_detector = FrameDetector()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_drop_detection()
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))
