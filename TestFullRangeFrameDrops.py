import glob
import os
import time
import unittest
from FrameDetector import FrameDetector
from ObsController import ObsController


def test_for_frame_drops(*, video_path: str, expected_amount_of_frames: int, recording_frame_rate: str = '60FPS',
                         playback_frame_rate: float, recording_length: int):

    list_of_supported_frame_rates = [24, 25, 29.97, 30, 50, 59.94, 60]

    if playback_frame_rate not in list_of_supported_frame_rates:
        raise Exception(str(playback_frame_rate) + ' is a not supported framerate or a typo.')
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
        expected_frames = 5000
        recording_frame_rate = '60FPS'
        playback_frame_rate = 60
        length_of_recording = 100
        amount_of_allowed_errors = 2
        frame_drops = test_for_frame_drops(video_path=path, expected_amount_of_frames=expected_frames,
                                           recording_frame_rate=recording_frame_rate,
                                           recording_length=length_of_recording,
                                           playback_frame_rate=playback_frame_rate)
        self.assertEqual(len(frame_drops), amount_of_allowed_errors, "Errors have been detected: " + str(frame_drops))
