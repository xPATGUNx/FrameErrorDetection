import os
import time


def test_data_file_writer(*, video_file_path, expected_amount_of_frames, scan_list):
    """
    Generates a text file and fills it with data from the passed list.
    """
    base_name = os.path.basename(video_file_path)
    timestr = time.strftime("%Y %m %d-%H%M%S")
    scan_data_name = ('Scan Results ' + timestr + str(base_name) + '.txt')
    scan_data_dir = ('Scan Results/' + scan_data_name)
    scan_data = open(scan_data_dir, 'w')
    scan_data.write('Detected frames in file "' + video_file_path + '":\n')

    for current_frame in range(1, expected_amount_of_frames + 1):
        occurrence = scan_list.count(current_frame)
        scan_data.write('Frame ' + str(current_frame) + ' occurred ' + str(occurrence) + ' times.\n')
    not_readable_frames = scan_list.count('QR code was not readable.')
    scan_data.write('QR code was not readable for ' + str(not_readable_frames) + ' frames.')
    scan_data.close()
    print('"' + scan_data_name + '"' + ' has been created.\n')


def list_frame_drops(*, expected_amount_of_frames, scan_list):
    frame_drop_index_list = []
    for current_frame in range(1, expected_amount_of_frames + 1):
        occurrence = scan_list.count(current_frame)
        if occurrence == 0:
            frame_drop_index_list.append(current_frame)
    return frame_drop_index_list


def list_frame_error_distances(*, frame_error_dict: dict):
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
        raise Exception('list_of_frame_drops needs at least 2 or more items. Items in list_of_frame_drops=' +
                        str(len(frame_error_dict)))


def index_of_first_frame_error(scan_list):
    first_frame_error = scan_list[0]
    return first_frame_error


def quality_metrics_report_writer(*, video_file_path: str, expected_amount_of_frames: int, scan_list, frame_error_dict):
    base_name = os.path.basename(video_file_path)
    metric_file_name = 'Quality Metrics for ' + str(base_name) + '.txt'
    metric_report_dir = 'Metric Reports/' + metric_file_name
    frame_drop_index_list = list_frame_drops(expected_amount_of_frames=expected_amount_of_frames, scan_list=scan_list)

    try:
        with open(metric_report_dir, 'w') as metric_report_writer:
            metric_report_writer.write('Quality Metrics for "' + str(base_name)+'":\n')
            metric_report_writer.write('\n')
            if len(frame_error_dict) == 0:
                metric_report_writer.write('No frame errors detected.')
            else:
                metric_report_writer.write('Total amount of frame errors: ' + str(len(frame_error_dict)) + '\n\n')
                amount_of_dropped_frames = len(frame_drop_index_list)
                metric_report_writer.write('Amount of dropped frames: ' + str(amount_of_dropped_frames) + '\n\n')
                metric_report_writer.write('Detected frame errors:\n')
                for frame, ocurrence in frame_error_dict.items():
                    metric_report_writer.write('Frame ' + str(frame) + ' occurred ' + str(ocurrence) + ' times.' + '\n')
                metric_report_writer.write('\n')
                if len(frame_error_dict) > 1:
                    frame_drop_distance_list = list_frame_error_distances(frame_error_dict=frame_error_dict)
                    metric_report_writer.write('Distances between frame errors:\n')
                    for distance in frame_drop_distance_list:
                        metric_report_writer.write(distance + '\n')
    finally:
        metric_report_writer.close()
