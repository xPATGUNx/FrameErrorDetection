import matplotlib.pyplot as plt
import math
import numpy as np


class DataVisualizer:

    @staticmethod
    def visualize_frame_scan(dictionary_of_frame_occurrences: dict, file_name: str):
        scan_dict = dictionary_of_frame_occurrences
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
        path = 'Visual Graphs/' + str(file_name) + '.png'
        fig.savefig(path, dpi=100)


test_dict = {
    1: 0,
    2: 3,
    3: 2,
    4: 2,
    5: 2,
    6: 3,
    7: 2
}

if __name__ == '__main__':
    DataVisualizer.visualize_frame_scan(test_dict, 'test')
