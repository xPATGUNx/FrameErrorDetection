import glob
import os
import time
import unittest
from FrameDetector import FrameDetector
from ObsController import ObsController


def test_for_frame_drops(*, video_path: str, expected_amount_of_frames: int, frame_rate: str, recording_length: int):
    obs = ObsController()
    try:
        obs.connect_with_obs()
        obs.set_profile(frame_rate)
        obs.set_video_directory(path=video_path)
        obs.record(recording_length)
    finally:
        obs.disconnect_with_obs()
    time.sleep(3)
    frame_detector = FrameDetector()
    list_of_files = glob.glob(video_path + '/*')
    latest_video_capture = max(list_of_files, key=os.path.getctime)
    frame_detector.set_video_analysis_parameters(latest_video_capture, expected_amount_of_frames)
    detected_frame_drops = frame_detector.frame_drop_detection(crop_video=True)
    return detected_frame_drops


class TestFrameDropDetection(unittest.TestCase):
    def test_30FPS_video_for_frame_drops(self):

        path = 'Video/TestFullRange'
        expected_frames = 150
        frame_rate = '60FPS'
        length_of_recording = 10
        frame_drops = test_for_frame_drops(video_path=path, expected_amount_of_frames=expected_frames,
                                           frame_rate=frame_rate, recording_length=length_of_recording)
        self.assertEqual(len(frame_drops), 2, "A problem has been detected: " + str(frame_drops))
