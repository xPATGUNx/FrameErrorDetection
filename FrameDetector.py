import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time
from collections import Counter
import typing


def qr_code_detection(video_file_path: str, expected_amount_of_frames):
    cap = cv.VideoCapture(video_file_path)
    timestr = time.strftime("%Y %m %d-%H%M%S")
    scan_data_name = ('QR Scan Results ' + timestr + '.txt')
    scan_data_dir = ('Scan Results/' + scan_data_name)
    scan_data = open(scan_data_dir, 'w')
    scan_data.write('Detected frames for file "' + video_file_path + '":\n')
    frame_index_list = []

    if not cap.isOpened():
        print("Error opening video stream or file")

    print('Scanning for frame IDs...')
    time.sleep(2)
    start = time.time()
    while cap.isOpened():

        ret, frame = cap.read()

        if ret:
            text_data = str(qr_code_scanner(frame))
            if not text_data == 'None':
                scan_data.write(text_data + '\n')
                frame_index_list.append(int(text_data))
            else:
                scan_data.write('QR-Code could not be found.\n')
        else:
            break

    print(frame_index_list)
    end = time.time()
    scan_data.close()
    cap.release()
    cv.destroyAllWindows()
    # print('Scan completed after ' + str(end - start) + ' seconds.')
    print('"' + scan_data_name + '"' + ' has been created.')
    # ToDo: replace magic number
    frame_counter(frame_index_list, expected_amount_of_frames)


def qr_code_scanner(obj):
    qr_code = decode(obj)
    for code in qr_code:
        data = code.data.decode('utf-8')
        # print(data)
        return data


def frame_counter(scan_list: list, amount_of_frames):
    for current_frame in range(amount_of_frames + 1):
        occurrance = scan_list.count(current_frame)
        print('Frame ' + str(current_frame) + ' occurred ' + str(occurrance) + ' times.')


if __name__ == '__main__':
    # qr_code_detection('Video/No_QR_Test.mp4', 180)
    # qr_code_detection('Video/QRCodeScreenCap.mp4', 180)
    qr_code_detection('Video/Mac Book Pro Capture.mp4', 180)
