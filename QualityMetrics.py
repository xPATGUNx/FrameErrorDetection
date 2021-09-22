import json
import os
import time
from DataVisualizer import *
from Utils import calc_current_time_code


def generate_report_data(*, video_file_path: str, expected_amount_of_frames: int, scan_list: list,
                         frame_error_dict: dict, frame_rate: float, frame_errors, frame_drops, frame_occurrences):
    base_name = os.path.basename(video_file_path)
    parent_dir = 'Reports'
    report_dir = f'Report for {base_name}'
    path_to_report = os.path.join(parent_dir, report_dir)
    os.mkdir(path_to_report)
    path_to_data = 'Data'
    data_folder = os.path.join(path_to_report, path_to_data)
    os.mkdir(data_folder)

    test_data_file_writer(report_dir=data_folder, video_file_path=video_file_path,
                          expected_amount_of_frames=expected_amount_of_frames,
                          scan_list=scan_list)

    quality_metrics_report_writer(report_dir=data_folder, video_file_path=video_file_path,
                                  expected_amount_of_frames=expected_amount_of_frames, scan_list=scan_list,
                                  frame_error_dict=frame_error_dict, frame_rate=frame_rate)

    store_data_in_json(report_dir=data_folder, video_file_path=video_file_path,
                       expected_amount_of_frames=expected_amount_of_frames, scan_list=scan_list,
                       frame_error_dict=frame_error_dict)

    data_visualizer = DataVisualizer()
    data_visualizer.set_parameters(report_dir=data_folder, video_file_path=video_file_path,
                                   dictionary_of_frame_occurrences=frame_occurrences,
                                   expected_amount_of_frames=expected_amount_of_frames,
                                   frame_errors=frame_errors,
                                   frame_drops=frame_drops)
    data_visualizer.visualize_frame_scan()
    data_visualizer.visualize_video_stats()


def test_data_file_writer(*, report_dir: str, video_file_path: str, expected_amount_of_frames: int, scan_list: list):
    """
    Generates a text file and fills it with data from the passed list.
    :param video_file_path: path to video file that is being tested.
    :param expected_amount_of_frames: An integer of the total amount of expected frames.
    :param scan_list: A list containing all detected frames.
    """
    base_name = os.path.basename(video_file_path)
    timestr: str = time.strftime("%Y %m %d-%H%M%S")
    scan_data_name = ('Scan Results ' + timestr + str(base_name) + '.txt')
    scan_data_dir = os.path.join(report_dir, scan_data_name)
    scan_data = open(scan_data_dir, 'w')
    scan_data.write('Detected frames in file "' + video_file_path + '":\n')

    for current_frame in range(1, expected_amount_of_frames + 1):
        occurrence = scan_list.count(current_frame)
        scan_data.write('Frame ' + str(current_frame) + ' occurred ' + str(occurrence) + ' times.\n')
    not_readable_frames = scan_list.count('QR code was not readable.')
    scan_data.write('QR code was not readable for ' + str(not_readable_frames) + ' frames.')
    scan_data.close()
    print('"' + scan_data_name + '"' + ' has been created.\n')


def list_frame_drops(*, expected_amount_of_frames: int, scan_list: list):
    """
    Lists all detected frame drops.
    :param expected_amount_of_frames: An integer of the total amount of expected frames.
    :param scan_list: A list containing all detected frames.
    :return: Returns a list containing integers representing the frame index of dropped frames.
    """
    frame_drop_index_list = []
    for current_frame in range(1, expected_amount_of_frames + 1):
        occurrence = scan_list.count(current_frame)
        if occurrence == 0:
            frame_drop_index_list.append(current_frame)
    return frame_drop_index_list


def list_frame_error_distances(*, frame_error_dict: dict):
    """
    Lists the distances between frame error indices.
    :param frame_error_dict: A dictionary containing the index of all frame errors.
    :return: Returns a list of strings containing information about the distance between frame errors
    """
    frame_error_dict = frame_error_dict
    frame_error_distances_list = []
    frame_error_index_list = []
    if len(frame_error_dict) > 1:
        frame_errors_index = frame_error_dict.keys()
        for items in frame_errors_index:
            frame_error_index_list.append(items)
        for i in range(len(frame_error_index_list) - 1):
            distance = frame_error_index_list[i + 1] - frame_error_index_list[i]
            frame_error_distances_list.append('Distance between frame error ' + str(frame_error_index_list[i]) +
                                              ' and ' + str(frame_error_index_list[i + 1]) + ': ' + str(distance))
        return frame_error_distances_list
    else:
        return None


def index_of_first_frame_error(scan_list):
    """
    A function to return the first frame error.
    :param scan_list: a list containing all detected frames.
    :return: Returns the first element of the scan list.
    """
    first_frame_error = scan_list[0]
    return first_frame_error


def quality_metrics_report_writer(*, report_dir: str, video_file_path: str, expected_amount_of_frames: int,
                                  scan_list: list, frame_error_dict: dict, frame_rate: float):
    """
    Generates a text file containing all quality metric results.
    :param report_dir: Path string to directory of storage.
    :param frame_rate: Set this float value to the frame rate of the test video that is being captured.
    :param video_file_path: path to video file that is being tested.
    :param expected_amount_of_frames: An integer of the total amount of expected frames.
    :param scan_list: A list containing all detected frames.
    :param frame_error_dict: A dictionary containing the index of all frame errors.
    """
    base_name = os.path.basename(video_file_path)
    metric_file_name = 'Quality Metrics for ' + str(base_name) + '.txt'
    metric_report_dir = os.path.join(report_dir, metric_file_name)
    frame_drop_index_list = list_frame_drops(expected_amount_of_frames=expected_amount_of_frames, scan_list=scan_list)

    try:
        with open(metric_report_dir, 'w') as metric_report_writer:
            metric_report_writer.write('Quality Metrics for "' + str(base_name) + '":\n')
            metric_report_writer.write('\n')
            if len(frame_error_dict) == 0:
                metric_report_writer.write('No frame errors detected.')
            else:
                metric_report_writer.write('Total amount of frame errors: ' + str(len(frame_error_dict)) + '\n\n')
                amount_of_dropped_frames = len(frame_drop_index_list)
                metric_report_writer.write('Amount of dropped frames: ' + str(amount_of_dropped_frames) + '\n\n')
                metric_report_writer.write('Detected frame errors:\n')
                for frame, occurrence in frame_error_dict.items():
                    occurrence_of_frame = occurrence[0]
                    time_code_position = calc_current_time_code(frame, frame_rate)
                    metric_report_writer.write('Frame ' + str(frame) + ' occurred ' + str(occurrence_of_frame) +
                                               ' times. Time Code position: ' + str(time_code_position) + '\n')
                metric_report_writer.write('\n')
                if len(frame_error_dict) > 1:
                    frame_drop_distance_list = list_frame_error_distances(frame_error_dict=frame_error_dict)
                    metric_report_writer.write('Distances between frame errors:\n')
                    for distance in frame_drop_distance_list:
                        metric_report_writer.write(distance + '\n')
    finally:
        metric_report_writer.close()


def store_data_in_json(*, report_dir: str, video_file_path: str, expected_amount_of_frames: int, scan_list,
                       frame_error_dict):
    base_name = os.path.basename(video_file_path)
    json_file_name = f'Report-data-for-{base_name}.json'
    json_file_dir = os.path.join(report_dir, json_file_name)
    report_title = f'Report for {base_name}'
    total_amount_of_errors = len(frame_error_dict)
    frame_drop_index_list = list_frame_drops(expected_amount_of_frames=expected_amount_of_frames, scan_list=scan_list)
    frame_drop_distance_list = list_frame_error_distances(frame_error_dict=frame_error_dict)
    total_amount_of_frame_drops = len(frame_drop_index_list)
    content = {
        'title': report_title,
        'total amount of frame errors': total_amount_of_errors,
        'total amount of frame drops': total_amount_of_frame_drops,
        'detected frame errors': frame_error_dict,
        'distances between frame errors': frame_drop_distance_list
    }
    json_string = json.dumps(content, indent=4)
    try:
        with open(json_file_dir, 'w') as json_file_writer:
            json_file_writer.writelines(json_string)
    finally:
        json_file_writer.close()
