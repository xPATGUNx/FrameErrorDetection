import glob
import os
import time
from DataVisualizer import DataVisualizer
from FrameErrorDetector import FrameErrorDetector
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

    frame_error_detector = FrameErrorDetector()
    data_visualizer = DataVisualizer()
    list_of_files = glob.glob(video_directory_path + '/*')
    latest_video_capture = max(list_of_files, key=os.path.getctime)
    frame_error_detector.set_video_analysis_parameters(latest_video_capture, expected_amount_of_frames)
    detected_frame_errors = frame_error_detector.frame_error_detection(crop_video=True,
                                                                       frames_per_second=playback_frame_rate)

    video_file_name = os.path.basename(frame_error_detector.video_file_path)
    occurrences_of_frames = frame_error_detector.dict_of_frame_occurrences
    frame_errors = len(detected_frame_errors)
    frame_drops = len(frame_error_detector.frame_drop_index_list)
    displayed_frames = expected_amount_of_frames - frame_drops
    data_visualizer.set_parameters(file_name=video_file_name,
                                   dictionary_of_frame_occurrences=occurrences_of_frames,
                                   expected_amount_of_frames=expected_amount_of_frames,
                                   displayed_frames=displayed_frames,
                                   frame_errors=frame_errors,
                                   frame_drops=frame_drops)
    data_visualizer.visualize_frame_scan()
    data_visualizer.visualize_video_stats()
    return detected_frame_errors
