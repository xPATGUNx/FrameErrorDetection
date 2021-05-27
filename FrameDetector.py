import os
import time

import cv2 as cv
from pyzbar.pyzbar import decode


class FrameDetector:
    def __init__(self):
        self.video_file_path = ''
        self.expected_amount_of_frames = 0
        self.scan_list = []

    def __qr_code_detection(self):
        """
        Iterates over every video frame individually and checks its QR code for frame index.
        :return: A list of every frame index.
        """
        cap = cv.VideoCapture(self.video_file_path)
        frame_index_list = []

        if not cap.isOpened():
            print("Error opening video stream or file")

        print('Scanning for frame IDs...')
        start = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                text_data = str(self.__qr_code_scanner(frame))
                if not text_data == 'None':
                    frame_index_list.append(int(text_data))
                else:
                    frame_index_list.append('QR code was not readable.')
            else:
                break
        end = time.time()
        cap.release()
        cv.destroyAllWindows()
        print('Scan completed after ' + str(end - start) + ' seconds.')
        self.scan_list = frame_index_list

    @staticmethod
    def __qr_code_scanner(frame):
        """
        A simple QR-Code scanner.
        :param frame: numpy.ndarray`, `PIL.Image` or tuple (pixels, width, height)
        :return: Returns the encoded data from the QR-Code
        """
        qr_code = decode(frame)
        for code in qr_code:
            data = code.data.decode('utf-8')
            # print(data)
            return data

    def __test_data_file_writer(self):
        """
        Generates a text file and fills it with data from the passed list.
        """
        base_name = os.path.basename(self.video_file_path)
        timestr = time.strftime("%Y %m %d-%H%M%S")
        scan_data_name = ('Scan Results ' + timestr + str(base_name) + '.txt')
        scan_data_dir = ('Scan Results/' + scan_data_name)
        scan_data = open(scan_data_dir, 'w')
        scan_data.write('Detected frames for file "' + self.video_file_path + '":\n')

        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence = self.scan_list.count(current_frame)
            scan_data.write('Frame ' + str(current_frame) + ' occurred ' + str(occurrence) + ' times.\n')
        not_readable_frames = self.scan_list.count('QR code was not readable.')
        scan_data.write('QR code was not readable for ' + str(not_readable_frames) + ' frames.')
        scan_data.close()
        print('"' + scan_data_name + '"' + ' has been created.')

    def __list_video_frame_errors(self):
        """
        Every frame has to occure only once. Every anomaly gets listed by this function.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence = self.scan_list.count(current_frame)
            if occurrence != 1:
                list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                  ' occurred ' + str(occurrence) + ' times.')
        return list_of_problematic_frames

    def set_parameters(self, video_file_path: str, expected_amount_of_frames: int):
        """
        Sets all parameters needed to use frame drop detection on a desired video.
        :param video_file_path: A string of the video_file_path to a video that needs to be analysed.
        :param expected_amount_of_frames: An integer with the exact amount of expected video frames to check against.
        :return:
        """
        self.video_file_path = video_file_path
        self.expected_amount_of_frames = expected_amount_of_frames

    def frame_drop_detection(self):
        """
        Core function to detect frame drops & frame duplicates in a video file.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        self.__qr_code_detection()
        self.__test_data_file_writer()
        list_of_detected_frame_drops = self.__list_video_frame_errors()
        return list_of_detected_frame_drops
