import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time
from collections import Counter
import typing
import os


def qr_code_detection(video_file_name: str, expected_amount_of_frames):
    cap = cv.VideoCapture('Video/' + video_file_name)
    frame_index_list = []

    if not cap.isOpened():
        print("Error opening video stream or file")

    print('Scanning for frame IDs...')
    start = time.time()
    while cap.isOpened():

        ret, frame = cap.read()

        if ret:
            text_data = str(qr_code_scanner(frame))
            if not text_data == 'None':
                frame_index_list.append(int(text_data))
            else:
                frame_index_list.append('QR code was not readable.')
        else:
            break

    # print(frame_index_list)
    end = time.time()
    cap.release()
    cv.destroyAllWindows()
    print('Scan completed after ' + str(end - start) + ' seconds.')

    # TODO: Extract these steps into another method
    test_data_file_writer(frame_index_list, expected_amount_of_frames, video_file_name)
    assert_frames_for_occurrences(frame_index_list, expected_amount_of_frames)
    return frame_index_list


def qr_code_scanner(obj):
    qr_code = decode(obj)
    for code in qr_code:
        data = code.data.decode('utf-8')
        # print(data)
        return data


def test_data_file_writer(scan_list: list, amount_of_frames, file_name):
    name_without_suffix = os.path.splitext(file_name)[0]
    timestr = time.strftime("%Y %m %d-%H%M%S")
    scan_data_name = (str(name_without_suffix) + ' Scan Results ' + timestr + '.txt')
    scan_data_dir = ('Scan Results/' + scan_data_name)
    scan_data = open(scan_data_dir, 'w')
    scan_data.write('Detected frames for file "' + file_name + '":\n')

    for current_frame in range(1, amount_of_frames + 1):
        occurrence = scan_list.count(current_frame)
        scan_data.write('Frame ' + str(current_frame) + ' occurred ' + str(occurrence) + ' times.\n')
    not_readable_frames = scan_list.count('QR code was not readable.')
    scan_data.write('QR code was not readable for ' + str(not_readable_frames) + ' frames.')
    scan_data.close()
    print('"' + scan_data_name + '"' + ' has been created.')


def assert_frames_for_occurrences(scan_list: list, amount_of_frames):
    list_of_problematic_frames = []
    for current_frame in range(1, amount_of_frames + 1):
        occurrence = scan_list.count(current_frame)
        if occurrence != 1:
            list_of_problematic_frames.append('Frame ' + str(current_frame) + ' occurred ' + str(occurrence) + ' times.')
    if len(list_of_problematic_frames) > 0:
        raise Exception('Warning! A problem has been detected: ' + str(list_of_problematic_frames))
    else:
        print('No Frame inconsistencies detected.')


if __name__ == '__main__':
    # qr_code_detection('No_QR_Test.mp4', 180)
    # qr_code_detection('QRCodeScreenCap.mp4', 180)
    qr_code_detection('MacBook Pro QuickTime Capture.mp4', 180)
    qr_code_detection('MacBook Pro Cubase  Capture 01.mp4', 180)
    qr_code_detection('MacBook Pro Cubase  Capture 02.mp4', 180)
