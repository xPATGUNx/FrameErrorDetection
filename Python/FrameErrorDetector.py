from Python.QualityMetrics import *
from Python.VideoScanner import VideoScanner


class FrameErrorDetector(VideoScanner):
    def __init__(self):
        super().__init__()

    # TODO: Refactor return statements to dictionaries
    def frame_error_detection(self, *, crop_video: bool = True, frames_per_second: float = 60):
        """
        Core function to detect frame drops & frame duplicates in a video file.
        The validation of 59 and 29 fps needs further evaluation. For now it is seen as equal to either 60 or 30 fps.
        :param frames_per_second: Set this float value equal to the frame rate of the playback video.
        :param crop_video: A boolean that toggles if the video is cropped to contain only the QR Code.
        Enabling this will significantly improve scan speed.
        :return: Returns a dictionary with all dropped or duplicated video frames.
        """
        self.scan_video_frames_for_id(crop_video=crop_video)
        if frames_per_second == 60:
            list_of_detected_frame_errors = self.__list_video_frame_errors_60_fps()
            return list_of_detected_frame_errors

        elif frames_per_second == 59.94:
            list_of_detected_frame_errors = self.__list_video_frame_errors_59_fps()
            return list_of_detected_frame_errors

        elif frames_per_second == 50:
            list_of_detected_frame_errors = self.__list_video_frame_errors_50_fps()
            return list_of_detected_frame_errors

        elif frames_per_second == 30:
            list_of_detected_frame_errors = self.__list_video_frame_errors_30_fps()
            return list_of_detected_frame_errors

        elif frames_per_second == 29.97:
            list_of_detected_frame_errors = self.__list_video_frame_errors_29_fps()
            return list_of_detected_frame_errors

        elif frames_per_second == 25:
            list_of_detected_frame_errors = self.__list_video_frame_errors_25_fps()
            return list_of_detected_frame_errors

        elif frames_per_second == 24:
            list_of_detected_frame_errors = self.__list_video_frame_errors_24_fps()
            return list_of_detected_frame_errors
        else:
            raise Exception(str(frames_per_second) + ' is a not supported framerate or a typo.')

    def __list_video_frame_errors_60_fps(self):
        """
        Every frame has to occur only once. Every anomaly gets listed by this function.
        :return: Returns a list with all dropped or duplicated video frames.
        """
        dictionary_of_frame_errors = {}
        for current_frame in range(1, self.expected_amount_of_frames + 1):
            occurrence_of_current_frame = self.video_frame_scan_list.count(current_frame)
            if occurrence_of_current_frame != 1:
                time_code = calc_current_time_code(current_frame, frame_rate=60)
                dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
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
                time_code = calc_current_time_code(current_frame, frame_rate=59.94)
                dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)

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
                        time_code = calc_current_time_code(current_frame, frame_rate=50)
                        dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
                else:
                    time_code = calc_current_time_code(current_frame, frame_rate=50)
                    dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
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
                time_code = calc_current_time_code(current_frame, frame_rate=30)
                dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
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
                time_code = calc_current_time_code(current_frame, frame_rate=29.97)
                dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)

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
                        time_code = calc_current_time_code(current_frame, frame_rate=25)
                        dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
                else:
                    time_code = calc_current_time_code(current_frame, frame_rate=25)
                    dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
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
                        time_code = calc_current_time_code(current_frame, frame_rate=24)
                        dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
                else:
                    time_code = calc_current_time_code(current_frame, frame_rate=24)
                    dictionary_of_frame_errors[current_frame] = (occurrence_of_current_frame, time_code)
        return dictionary_of_frame_errors
