import unittest
from Python.TestFullRangeFrameDrops import *


class TestFrameDropDetection(unittest.TestCase):
    """
    An example python test class for a Frame Error Detection Test run.
    """
    def test_video_capture_for_frame_drops(self):
        name_of_test_run = 'Example Test'   # Name of test run
        path = 'D:/Captured Video'          # Path to video capture directory
        report_path = '../Reports'          # Path of report storage
        expected_frames = 5000              # Total amount of expected video frames
        recording_frame_rate = '60FPS'      # Capture framerate (to simulate a consumer display set this to '60FPS')
        playback_frame_rate = 60            # Framerate of video playback
        length_of_recording = 100           # Duration of recording in seconds
        amount_of_allowed_errors = 0        # Amount of tolerated frame errors
        frame_errors = test_for_frame_errors(video_directory_path=path,
                                             expected_amount_of_frames=expected_frames,
                                             recording_frame_rate=recording_frame_rate,
                                             recording_length=length_of_recording,
                                             playback_frame_rate=playback_frame_rate,
                                             open_report=True,
                                             name_of_test_run=name_of_test_run,
                                             report_path=report_path)
        error_count = len(frame_errors)
        self.assertTrue(error_count <= amount_of_allowed_errors, "Errors have been detected: " + str(frame_errors))
