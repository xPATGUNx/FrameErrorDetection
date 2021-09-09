import matplotlib.pyplot as plt
import math
import numpy as np


class DataVisualizer:

    def __init__(self):
        self.file_name = ''
        self.dictionary_of_frame_occurrences = {}
        self.expected_amount_of_frames = 0
        self.displayed_frames = 0
        self.frame_errors = 0
        self.frame_drops = 0

    def set_parameters(self, *, file_name: str, dictionary_of_frame_occurrences: dict, expected_amount_of_frames: int,
                       displayed_frames: int, frame_errors: int, frame_drops: int) -> None:
        self.file_name = file_name
        self.dictionary_of_frame_occurrences = dictionary_of_frame_occurrences
        self.expected_amount_of_frames = expected_amount_of_frames
        self.displayed_frames = displayed_frames
        self.frame_errors = frame_errors
        self.frame_drops = frame_drops

    def visualize_frame_scan(self):
        scan_dict = self.dictionary_of_frame_occurrences
        x = scan_dict.keys()
        y = scan_dict.values()
        y_int = range(min(y), math.ceil(max(y)) + 1)

        plt.yticks(y_int)
        plt.plot(x, y)
        plt.title('Occurrences of frames')
        plt.xlabel('Frame')
        plt.ylabel('Occurrence')
        plt.axis([0, len(x), 0, 8])
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        path = 'Visual Graphs/Occurrence Graphs/Occurrence Graph ' + str(self.file_name) + '.png'
        fig.savefig(path, dpi=100)

    def visualize_video_stats(self):

        percentage_of_displayed = (self.displayed_frames / self.expected_amount_of_frames) * 100
        percentage_of_errors = (self.frame_errors / self.expected_amount_of_frames) * 100
        percentage_of_drops = (self.frame_drops / self.expected_amount_of_frames) * 100

        plt.rcdefaults()
        fig, ax = plt.subplots()

        bars = ('Displayed\n Frames\n' + str(percentage_of_displayed) + '%',
                'Frame\n Errors\n' + str(percentage_of_errors) + '%',
                'Dropped\n Frames\n' + str(percentage_of_drops) + '%')
        y_pos = np.arange(len(bars))
        performance = [percentage_of_displayed, percentage_of_errors, percentage_of_drops]

        ax.barh(y_pos, performance, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(bars)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Amount of frames in %')
        ax.set_title('Frame Display Stats')

        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        path = 'Visual Graphs/Frame Stats/Frame Stats ' + str(self.file_name) + '.png'
        fig.savefig(path, dpi=100)
