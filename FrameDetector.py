import os
import time

import cv2 as cv
import pyzbar.pyzbar as pyzbar
import numpy as np
from QualityMetrics import *


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
                    # print(int(text_data))
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

    def set_video_analysis_parameters(self, video_file_path: str, expected_amount_of_frames: int):
        """
        Sets all parameters needed to use frame drop detection on a desired video.
        :param video_file_path: A string of the video_file_path to a video that needs to be analysed.
        :param expected_amount_of_frames: An integer with the exact amount of expected video frames to check against.
        :return:
        """
        self.video_file_path = video_file_path
        self.expected_amount_of_frames = expected_amount_of_frames

    def frame_drop_detection(self, crop_video: bool = True, frames_per_second: float = None):
        """
        Core function to detect frame drops & frame duplicates in a video file.
        The validation of 59 and 29 fps needs further evaluation. For now it is seen as equal to either 60 or 30 fps.
        :param frames_per_second: Set this float value equal to the frame rate of the playback video.
        :param crop_video: A boolean that toggles if the video is cropped to contain only the QR Code.
        Enabling this will significantly improve scan speed.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        self.__qr_code_detection(crop_video=crop_video)
        test_data_file_writer(video_file_path=self.video_file_path,
                              expected_amount_of_frames=self.expected_amount_of_frames,
                              scan_list=self.scan_list)

        if frames_per_second is None or frames_per_second == 60:
            list_of_detected_frame_drops = self.__list_video_frame_errors_default()
            return list_of_detected_frame_drops
        elif frames_per_second == 59.94:
            list_of_detected_frame_drops = self.__list_video_frame_errors_59_fps()
            return list_of_detected_frame_drops
        elif frames_per_second == 50:
            list_of_detected_frame_drops = self.__list_video_frame_errors_50_fps()
            return list_of_detected_frame_drops
        elif frames_per_second == 30:
            list_of_detected_frame_drops = self.__list_video_frame_errors_30_fps()
            return list_of_detected_frame_drops
        elif frames_per_second == 29.97:
            list_of_detected_frame_drops = self.__list_video_frame_errors_29_fps()
            return list_of_detected_frame_drops
        elif frames_per_second == 25:
            list_of_detected_frame_drops = self.__list_video_frame_errors_25_fps()
            return list_of_detected_frame_drops
        elif frames_per_second == 24:
            list_of_detected_frame_drops = self.__list_video_frame_errors_24_fps()
            return list_of_detected_frame_drops
        else:
            raise Exception(str(frames_per_second) + ' is a not supported framerate or a typo.')

    def crop_frame(self, frame: np.ndarray, margin: int = 1):
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

    def __list_video_frame_errors_default(self):
        """
        Every frame has to occure only once. Every anomaly gets listed by this function.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            if occurrence_of_current_frame != 1:
                list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                  ' occurred ' + str(occurrence_of_current_frame) + ' times.')
        return list_of_problematic_frames

    def __list_video_frame_errors_59_fps(self):
        """
                Lists every frame error that happens during recording of video playback in 59.94 fps.
                :return: Returns a list with all dropped or duplicated video frames.
                """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            if occurrence_of_current_frame != 1 and occurrence_of_current_frame != 2:
                list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                  ' occurred ' + str(occurrence_of_current_frame) + ' times.')

        return list_of_problematic_frames

    def __list_video_frame_errors_50_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 50 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            occurrence_of_previous_frame = self.scan_list.count(current_frame - 1)
            occurrence_of_next_frame = self.scan_list.count(current_frame + 1)

            if occurrence_of_current_frame != 1:
                if occurrence_of_current_frame == 2:
                    if occurrence_of_previous_frame != 1 and occurrence_of_next_frame != 1 \
                            and current_frame != self.expected_amount_of_frames and current_frame - 1 != 0:
                        list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                          ' occurred ' + str(occurrence_of_current_frame) + ' times.')
                else:
                    list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                      ' occurred ' + str(occurrence_of_current_frame) + ' times.')
        return list_of_problematic_frames

    def __list_video_frame_errors_30_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 30 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            if occurrence_of_current_frame != 2:
                list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                  ' occurred ' + str(occurrence_of_current_frame) + ' times.')
        return list_of_problematic_frames

    def __list_video_frame_errors_29_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 29.97 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            if occurrence_of_current_frame != 1 and occurrence_of_current_frame != 2 \
                    and occurrence_of_current_frame != 3:
                list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                  ' occurred ' + str(occurrence_of_current_frame) + ' times.')

        return list_of_problematic_frames

    def __list_video_frame_errors_25_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 25 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            occurrence_of_previous_frame = self.scan_list.count(current_frame - 1)
            occurrence_of_next_frame = self.scan_list.count(current_frame + 1)

            if occurrence_of_current_frame != 2:
                if occurrence_of_current_frame == 3:
                    if occurrence_of_previous_frame != 2 and occurrence_of_next_frame != 2 \
                            and current_frame != self.expected_amount_of_frames and current_frame - 1 != 0:
                        list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                          ' occurred ' + str(occurrence_of_current_frame) + ' times.')
                else:
                    list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                      ' occurred ' + str(occurrence_of_current_frame) + ' times.')
        return list_of_problematic_frames

    def __list_video_frame_errors_24_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 24 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        list_of_problematic_frames = []
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.scan_list.count(current_frame)
            occurrence_of_previous_frame = self.scan_list.count(current_frame - 1)
            occurrence_of_next_frame = self.scan_list.count(current_frame + 1)

            if occurrence_of_current_frame != 2:
                if occurrence_of_current_frame == 3:
                    if occurrence_of_previous_frame != (2 or 3) and occurrence_of_next_frame != (2 or 3) \
                            and current_frame != self.expected_amount_of_frames and current_frame - 1 != 0:
                        list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                          ' occurred ' + str(occurrence_of_current_frame) + ' times.')
                else:
                    list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                      ' occurred ' + str(occurrence_of_current_frame) + ' times.')
        return list_of_problematic_frames


"""
NOTES:
pattern for 50 fps:
            if current_frame % 25 == 1 or current_frame % 25 == 6 or current_frame % 25 == 10 or current_frame % 25 == 16 or current_frame % 25 == 20:
                if occurrence != 2:
                    list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                      ' occurred ' + str(occurrence) + ' times. Expected: 2')
"""
