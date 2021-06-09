import os
import time

import cv2 as cv
import pyzbar.pyzbar as pyzbar
import numpy as np


class FrameDetector:
    def __init__(self):
        self.video_file_path = ''
        self.expected_amount_of_frames = 0
        self.scan_list = []
        self.__qr_code_position = None

    def __find_position_of_qr_code(self):
        cap = cv.VideoCapture(self.video_file_path)
        print('Scanning for QR Code location...')
        start = time.time()
        if not cap.isOpened():
            print("Error opening video stream or file")
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                # print(self.__qr_code_scanner(gray_frame, return_position=True))
                qr_code_coordinates = self.__qr_code_scanner(gray_frame, return_position=True)
                if qr_code_coordinates is not None:
                    self.__qr_code_position = qr_code_coordinates
                    end = time.time()
                    print('Position of QR Code has been detected after ' + str(end - start) + ' seconds.')
                    break
            else:
                break
        cap.release()
        cv.destroyAllWindows()

    def __qr_code_detection(self, crop_video: bool = True):
        """
        Iterates over every video frame individually and checks its QR code for frame index.
        :return: A list of every frame index.
        """
        self.__find_position_of_qr_code()
        cap = cv.VideoCapture(self.video_file_path)
        frame_index_list = []
        if not cap.isOpened():
            print("Error opening video stream or file")

        print('Scanning for frame IDs...')
        start = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if crop_video:
                    video_frame = self.crop_frame(frame)
                else:
                    video_frame = frame
                gray_frame = cv.cvtColor(video_frame, cv.COLOR_BGR2GRAY)
                text_data = str(self.__qr_code_scanner(gray_frame))
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
    def __qr_code_scanner(frame: np.ndarray, return_position: bool = False):
        """
        A simple QR-Code scanner.
        :param frame: numpy.ndarray`, `PIL.Image` or tuple (pixels, width, height)
        :return: Returns the encoded data from the QR-Code
        """
        if return_position:
            qr_code = pyzbar.decode(frame)
            for location in qr_code:
                (x, y, w, h) = location.rect
                return x, y, w, h
        else:
            qr_code = pyzbar.decode(frame)
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
        print('"' + scan_data_name + '"' + ' has been created.\n')

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

    def set_video_analysis_parameters(self, video_file_path: str, expected_amount_of_frames: int):
        """
        Sets all parameters needed to use frame drop detection on a desired video.
        :param video_file_path: A string of the video_file_path to a video that needs to be analysed.
        :param expected_amount_of_frames: An integer with the exact amount of expected video frames to check against.
        :return:
        """
        self.video_file_path = video_file_path
        self.expected_amount_of_frames = expected_amount_of_frames

    def frame_drop_detection(self, crop_video: bool = True):
        """
        Core function to detect frame drops & frame duplicates in a video file.
        :param crop_video: A boolean that toggles if the video is cropped to contain only the QR Code.
        Enabling this will significantly improve scan speed.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        self.__qr_code_detection(crop_video=crop_video)
        self.__test_data_file_writer()
        list_of_detected_frame_drops = self.__list_video_frame_errors()
        return list_of_detected_frame_drops

    def crop_frame(self, frame: np.ndarray, margin: int = 0):
        """
        Crops current frame to only contain the QR Code.
        :param frame: numpy.ndarray`, `PIL.Image` or tuple (pixels, width, height)
        :param margin: An integer that manipulates the cropping margin.
        :return: Returns a cropped version of the current video frame.
        """
        x, y, w, h = self.__qr_code_position
        m = margin
        cropped_frame = frame[y - m:y + h + m, x - m:x + w + m]
        return cropped_frame
