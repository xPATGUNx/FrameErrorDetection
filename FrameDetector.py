import cv2 as cv
import numpy as np
from QualityMetrics import *
from Utils import qr_code_scanner


class FrameDetector:
    """
    Core class for detection of frame errors.
    """
    def __init__(self):
        self.video_file_path = ''
        self.expected_amount_of_frames = 0
        self.video_frame_scan_list = []
        self.__qr_code_position = None

    def set_video_analysis_parameters(self, video_file_path: str, expected_amount_of_frames: int):
        """
        Sets all parameters needed to use frame drop detection on a desired video.
        :param video_file_path: A string of the video_file_path to a video that needs to be analysed.
        :param expected_amount_of_frames: An integer with the exact amount of expected video frames to check against.
        """
        self.video_file_path = video_file_path
        self.expected_amount_of_frames = expected_amount_of_frames

    def __find_position_of_qr_code(self) -> None:
        """
        Iterates over video frames until the QR code is found.
        The position of the QR code is then saved to self.__qr_code_position.
        """
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
                qr_code_coordinates = qr_code_scanner(gray_frame, return_position=True)
                if qr_code_coordinates is not None:
                    self.__qr_code_position = qr_code_coordinates
                    end = time.time()
                    print('Position of QR Code has been detected after ' + str(end - start) + ' seconds.')
                    break
            else:
                break
        cap.release()
        cv.destroyAllWindows()

    def scan_video_frames_for_id(self, crop_video: bool = True):
        """
        Iterates over every video frame individually and checks its QR code for frame index.
        A list of every frame index is saved to self.video_frame_scan_list.
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
                text_data = str(qr_code_scanner(gray_frame))
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
        self.video_frame_scan_list = frame_index_list

    def frame_drop_detection(self, *, crop_video: bool = True, frames_per_second: float = 60):
        """
        Core function to detect frame drops & frame duplicates in a video file.
        The validation of 59 and 29 fps needs further evaluation. For now it is seen as equal to either 60 or 30 fps.
        :param frames_per_second: Set this float value equal to the frame rate of the playback video.
        :param crop_video: A boolean that toggles if the video is cropped to contain only the QR Code.
        Enabling this will significantly improve scan speed.
        :return: Returns a dictionary with all dropped or duplicated video frames.
        """
        self.scan_video_frames_for_id(crop_video=crop_video)
        test_data_file_writer(video_file_path=self.video_file_path,
                              expected_amount_of_frames=self.expected_amount_of_frames,
                              scan_list=self.video_frame_scan_list)
        if frames_per_second == 60:
            list_of_detected_frame_drops = self.__list_video_frame_errors_60_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
            return list_of_detected_frame_drops
        elif frames_per_second == 59.94:
            list_of_detected_frame_drops = self.__list_video_frame_errors_59_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
            return list_of_detected_frame_drops
        elif frames_per_second == 50:
            list_of_detected_frame_drops = self.__list_video_frame_errors_50_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
            return list_of_detected_frame_drops
        elif frames_per_second == 30:
            list_of_detected_frame_drops = self.__list_video_frame_errors_30_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
            return list_of_detected_frame_drops
        elif frames_per_second == 29.97:
            list_of_detected_frame_drops = self.__list_video_frame_errors_29_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
            return list_of_detected_frame_drops
        elif frames_per_second == 25:
            list_of_detected_frame_drops = self.__list_video_frame_errors_25_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
            return list_of_detected_frame_drops
        elif frames_per_second == 24:
            list_of_detected_frame_drops = self.__list_video_frame_errors_24_fps()
            quality_metrics_report_writer(video_file_path=self.video_file_path,
                                          expected_amount_of_frames=self.expected_amount_of_frames,
                                          scan_list=self.video_frame_scan_list,
                                          frame_error_dict=list_of_detected_frame_drops,
                                          frame_rate=frames_per_second)
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

    def __list_video_frame_errors_60_fps(self):
        """
        Every frame has to occure only once. Every anomaly gets listed by this function.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            if occurrence_of_current_frame != 1:
                dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
        return dictionary_of_frame_errors

    def __list_video_frame_errors_59_fps(self):
        """
                Lists every frame error that happens during recording of video playback in 59.94 fps.
                :return: Returns a list with all dropped or duplicated video frames.
                """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            if occurrence_of_current_frame != 1 and occurrence_of_current_frame != 2:
                dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame

        return dictionary_of_frame_errors

    def __list_video_frame_errors_50_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 50 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            occurrence_of_previous_frame = self.video_frame_scan_list.count(current_frame - 1)
            occurrence_of_next_frame = self.video_frame_scan_list.count(current_frame + 1)

            if occurrence_of_current_frame != 1:
                if occurrence_of_current_frame == 2:
                    if occurrence_of_previous_frame != 1 and occurrence_of_next_frame != 1 \
                            and current_frame != self.expected_amount_of_frames and current_frame - 1 != 0:
                        dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
                else:
                    dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
        return dictionary_of_frame_errors

    def __list_video_frame_errors_30_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 30 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            if occurrence_of_current_frame != 2:
                dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
        return dictionary_of_frame_errors

    def __list_video_frame_errors_29_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 29.97 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            if occurrence_of_current_frame != 1 and occurrence_of_current_frame != 2 \
                    and occurrence_of_current_frame != 3:
                dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame

        return dictionary_of_frame_errors

    def __list_video_frame_errors_25_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 25 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            occurrence_of_previous_frame = self.video_frame_scan_list.count(current_frame - 1)
            occurrence_of_next_frame = self.video_frame_scan_list.count(current_frame + 1)

            if occurrence_of_current_frame != 2:
                if occurrence_of_current_frame == 3:
                    if occurrence_of_previous_frame != 2 and occurrence_of_next_frame != 2 \
                            and current_frame != self.expected_amount_of_frames and current_frame - 1 != 0:
                        dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
                else:
                    dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
        return dictionary_of_frame_errors

    def __list_video_frame_errors_24_fps(self):
        """
        Lists every frame error that happens during recording of video playback in 24 fps.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            occurrence_of_previous_frame = self.video_frame_scan_list.count(current_frame - 1)
            occurrence_of_next_frame = self.video_frame_scan_list.count(current_frame + 1)

            if occurrence_of_current_frame != 2:
                if occurrence_of_current_frame == 3:
                    if occurrence_of_previous_frame != (2 or 3) and occurrence_of_next_frame != (2 or 3) \
                            and current_frame != self.expected_amount_of_frames and current_frame - 1 != 0:
                        dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
                else:
                    dictionary_of_frame_errors[current_frame] = occurrence_of_current_frame
        return dictionary_of_frame_errors
