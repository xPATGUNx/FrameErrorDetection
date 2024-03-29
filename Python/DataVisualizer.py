import os.path
import matplotlib.pyplot as plt
import math
import numpy as np


class DataVisualizer:
    """
    Class for visualisation of test data.
    """
    def __init__(self):
        self.report_dir = ''
        self.file_name = ''
        self.dictionary_of_frame_occurrences = {}
        self.expected_amount_of_frames = 0
        self.frame_errors = 0
        self.frame_drops = 0

    def set_parameters(self, *, report_dir: str, dictionary_of_frame_occurrences: dict,
                       expected_amount_of_frames: int,
                       frame_errors: int, frame_drops: int) -> None:
        """
        Setter function for class variables.
        :param report_dir: A string of the desired path of report storage
        :param dictionary_of_frame_occurrences: A dictionary containing all detected frames.
        :param expected_amount_of_frames: An integer representing the total amount of expected frames.
        :param frame_errors: An integer of the total amount of detected frame errors.
        :param frame_drops: An integer of the total amount of detected frame drops.
        """
        self.report_dir = report_dir
        self.dictionary_of_frame_occurrences = dictionary_of_frame_occurrences
        self.expected_amount_of_frames = expected_amount_of_frames
        self.frame_errors = frame_errors
        self.frame_drops = frame_drops

    def visualize_frame_scan(self):
        """
        Use this function to plot a visualisation of the frame scan results as a line graph.
        Plot will be saved as a PNG file in the set report directory.
        """
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

        file_name = f'Occurrence Graph.png'
        path = os.path.join(self.report_dir, file_name)
        self._plot_graphic(path)

    def visualize_video_stats(self):
        """
        Use this function to plot a visualisation of the frame stats as a bar graph.
        Plot will be saved as a PNG file in the set report directory.
        """
        displayed_frames = self.expected_amount_of_frames - self.frame_drops
        percentage_of_displayed = (displayed_frames / self.expected_amount_of_frames) * 100
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

        file_name = f'Frame Stats.png'
        path = os.path.join(self.report_dir, file_name)
        self._plot_graphic(path)

    @staticmethod
    def _plot_graphic(path: str, width: float = 18.5, height: float = 10.5):
        """
        This function is called to plot the graphic.
        :param path: a string of the path to save location.
        :param width: a float value of the width of the image.
        :param height: a float value of the height of the image.
        """
        fig = plt.gcf()
        fig.set_size_inches(width, height)
        fig.savefig(path, dpi=100)
