import glob
import os
import time
import unittest
from VideoScanner import VideoScanner
from ObsController import ObsController


def test_for_frame_errors(*, video_directory_path: str, expected_amount_of_frames: int,
                          recording_frame_rate: str = '60FPS', playback_frame_rate: float, recording_length: int):
    """
    Main function to perform a video capture test for frame errors.
    :param video_directory_path: A string containing the path to the video capture directory.
    :param expected_amount_of_frames: An integer of the total amount of expected frames.
    :param recording_frame_rate:
    This parameter sets via a String the recording frame rate by changing the current profile in OBS.
    Currently available profile are: '60FPS', '59.94FPS', '50FPS', '30FPS', '29.97FPS', '25FPS', '24FPS'.
    :param playback_frame_rate: A float value that has to be set equal to the frame rate of the video playback.
    :param recording_length: An integer that sets the length of recording in Seconds
    :return: Returns a dictionary with all dropped or duplicated video frames.
    """

    list_of_supported_frame_rates = [24, 25, 29.97, 30, 50, 59.94, 60]

    if playback_frame_rate not in list_of_supported_frame_rates:
        raise Exception(str(playback_frame_rate) + ' is a not supported framerate or a typo.')
    obs = ObsController()
    try:
        obs.connect_with_obs()
        obs.set_profile(recording_frame_rate)
        time.sleep(3)
        obs.set_video_directory(path=video_directory_path)
        obs.record(recording_length)
    finally:
        obs.disconnect_with_obs()
    time.sleep(5)
    frame_detector = VideoScanner()
    list_of_files = glob.glob(video_directory_path + '/*')
    latest_video_capture = max(list_of_files, key=os.path.getctime)
    frame_detector.set_video_analysis_parameters(latest_video_capture, expected_amount_of_frames)
    detected_frame_errors = frame_detector.frame_drop_detection(crop_video=True, frames_per_second=playback_frame_rate)
    return detected_frame_errors


class TestFrameDropDetection(unittest.TestCase):
    def test_video_capture_for_frame_drops(self):
        path = 'D:/Captured Video'      # Path to video capture directory
        expected_frames = 5000          # Total amount of expected video frames
        recording_frame_rate = '60FPS'  # Capture framerate (to simulate a consumer display set this to '60FPS')
        playback_frame_rate = 24        # Framerate of video playback
        length_of_recording = 250       # Duration of recording in seconds
        amount_of_allowed_errors = 2    # Amount of tolerated frame errors
        frame_errors = test_for_frame_errors(video_directory_path=path, expected_amount_of_frames=expected_frames,
                                             recording_frame_rate=recording_frame_rate,
                                             recording_length=length_of_recording,
                                             playback_frame_rate=playback_frame_rate)
        error_count = len(frame_errors)
        self.assertEqual(error_count, amount_of_allowed_errors, "Errors have been detected: " + str(frame_errors))
