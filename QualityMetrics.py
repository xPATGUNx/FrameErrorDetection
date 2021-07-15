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
    scan_data.write('Detected frames for file "' + video_file_path + '":\n')

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


def construct_frame_drop_distances_dictionary(*, list_of_frame_drops: list):
    list_of_frame_drops = list_of_frame_drops
    frame_drop_distance_dictionary = {}
    if len(list_of_frame_drops) > 1:
        for i in range(len(list_of_frame_drops) - 1):
            distance = list_of_frame_drops[i] - list_of_frame_drops[i+1]
            frame_drop_distance_dictionary['Frame drop distance ' + str(i)] = distance
        return frame_drop_distance_dictionary
    else:
        raise Exception('list_of_frame_drops needs at least 2 or more items. list_of_frame_drops=' +
                        str(len(list_of_frame_drops)))


def index_of_first_frame_error(scan_list):
    first_frame_error = scan_list[0]
    return first_frame_error
