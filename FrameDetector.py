import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time


def qr_code_detection(video_file_path):
    cap = cv.VideoCapture(video_file_path)
    timestr = time.strftime("%Y %m %d-%H%M%S")
    scan_data_name = ('QR Scan Results ' + timestr + '.txt')
    scan_data_dir = ('Scan Results/' + scan_data_name)
    scan_data = open(scan_data_dir, 'w')
    scan_data.write('Detected frames for file "' + video_file_path + '":\n')

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
            else:
                scan_data.write('QR-Code could not be found.\n')
        else:
            break

    end = time.time()
    scan_data.close()
    cap.release()
    cv.destroyAllWindows()
    print('Scan completed after ' + str(end - start) + ' seconds.')
    print('"' + scan_data_name + '"' + ' has been created.')


def qr_code_scanner(obj):
    qr_code = decode(obj)
    for code in qr_code:
        data = code.data.decode('utf-8')
        print(data)
        return data


if __name__ == '__main__':
    qr_code_detection('Video/No_QR_Test.mp4')
