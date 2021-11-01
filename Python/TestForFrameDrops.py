import unittest
from Python.VideoScanner import VideoScanner


class TestFrameDropDetection(unittest.TestCase):
    def test_60FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_60FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_59FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_59.97FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_50FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_50FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_30FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_30FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_29FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_29.97FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_25FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_25FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_24FPS_video_for_frame_drops(self):
        video = 'Video/QR_Code_Videos/QR_150_Frames_24FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_videos_for_frame_drops(self):
        video = 'Video/Elgato/60 FPS.mp4'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=True)
        self.assertNotEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_mkv_video_for_frame_drops(self):
        video = 'Video/Elgato/60 FPS.mkv'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection()
        self.assertNotEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_2h_video_for_frame_drops(self):
        video = 'Video/QR_Code_Frame_180587Frames_25FPS.mp4'
        expected_video_frames = 180586
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection()
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))

    def test_capture_for_frame_drops(self):
        video = 'Video/Elgato 30 FPS Lenovo 3.mkv'
        expected_video_frames = 150
        frame_detector = VideoScanner()
        frame_detector.set_video_analysis_parameters(video, expected_video_frames)
        detected_frame_drops = frame_detector.frame_error_detection(crop_video=False)
        self.assertEqual(len(detected_frame_drops), 0, "A problem has been detected: " + str(detected_frame_drops))