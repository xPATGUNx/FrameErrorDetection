import unittest
from Python.TestFullRangeFrameDrops import *


# TODO: Add Pydoc
class TestFrameDropDetection(unittest.TestCase):
    def test_video_capture_for_frame_drops(self):
        path = 'D:/Captured Video'      # Path to video capture directory
        expected_frames = 5000          # Total amount of expected video frames
        recording_frame_rate = '60FPS'  # Capture framerate (to simulate a consumer display set this to '60FPS')
        playback_frame_rate = 60        # Framerate of video playback
        length_of_recording = 100       # Duration of recording in seconds
        amount_of_allowed_errors = 0    # Amount of tolerated frame errors
        frame_errors = test_for_frame_errors(video_directory_path=path, expected_amount_of_frames=expected_frames,
                                             recording_frame_rate=recording_frame_rate,
                                             recording_length=length_of_recording,
                                             playback_frame_rate=playback_frame_rate)
        error_count = len(frame_errors)
        self.assertTrue(error_count <= amount_of_allowed_errors, "Errors have been detected: " + str(frame_errors))