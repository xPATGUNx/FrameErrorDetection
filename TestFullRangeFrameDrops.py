import glob
import os
import time
import unittest
from FrameDetector import FrameDetector
from ObsController import ObsController


def test_for_frame_drops(*, video_path: str, expected_amount_of_frames: int, recording_frame_rate: str = '60FPS',
                         playback_frame_rate: float, recording_length: int):
    obs = ObsController()
    try:
        obs.connect_with_obs()
        obs.set_profile(recording_frame_rate)
        time.sleep(3)
        obs.set_video_directory(path=video_path)
        obs.record(recording_length)
    finally:
        obs.disconnect_with_obs()
    time.sleep(5)
    frame_detector = FrameDetector()
    list_of_files = glob.glob(video_path + '/*')
    latest_video_capture = max(list_of_files, key=os.path.getctime)
    frame_detector.set_video_analysis_parameters(latest_video_capture, expected_amount_of_frames)
    detected_frame_drops = frame_detector.frame_drop_detection(crop_video=True, frames_per_second=playback_frame_rate)
    return detected_frame_drops


class TestFrameDropDetection(unittest.TestCase):
    def test_video_capture_for_frame_drops(self):

        path = 'D:/Captured Video'
        expected_frames = 150
        recording_frame_rate = '60FPS'
        playback_frame_rate = 30
        length_of_recording = 10
        frame_drops = test_for_frame_drops(video_path=path, expected_amount_of_frames=expected_frames,
                                           recording_frame_rate=recording_frame_rate,
                                           recording_length=length_of_recording,
                                           playback_frame_rate=playback_frame_rate)
        self.assertEqual(len(frame_drops), 2, "Errors have been detected: " + str(frame_drops))
