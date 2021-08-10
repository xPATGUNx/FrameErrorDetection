import cv2 as cv
import numpy as np
import time
from Utils import qr_code_scanner


class VideoScanner:
    """
    Core class for detection of frame errors.
    """
    def __init__(self):
        self.video_file_path = ''
        self.expected_amount_of_frames = 0
        self.video_frame_scan_list = []
        self.dict_of_frame_occurrences = {}
        self.__qr_code_position = None

    def set_video_analysis_parameters(self, video_file_path: str, expected_amount_of_frames: int):
        """
        Sets all parameters needed to use frame drop detection on a desired video.
        :param video_file_path: A string of the video_file_path to a video that needs to be analysed.
        :param expected_amount_of_frames: An integer with the exact amount of expected video frames to check against.
        """
        self.video_file_path = video_file_path
        self.expected_amount_of_frames = expected_amount_of_frames

    def get_video_frame_scan_list(self):
        return self.video_frame_scan_list

    def find_position_of_qr_code(self) -> None:
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
        self.find_position_of_qr_code()
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
        self.create_dict_of_frame_occurrences()

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

    def create_dict_of_frame_occurrences(self):
        list_of_scanned_frames = self.video_frame_scan_list
        expected_amount_of_frames = self.expected_amount_of_frames
        dict_of_frame_occurrences = {}
        for current_frame in range(1, expected_amount_of_frames + 1):
            occurrence = list_of_scanned_frames.count(current_frame)
            dict_of_frame_occurrences[current_frame] = occurrence
        self.dict_of_frame_occurrences = dict_of_frame_occurrences
