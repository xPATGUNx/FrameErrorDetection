import numpy as np
import pyzbar.pyzbar as pyzbar


def qr_code_scanner(frame: np.ndarray, return_position: bool = False):
    """
    A simple QR-Code scanner that can be used to either read the QR-Code or simply return its position.
    :param frame: numpy.ndarray`, `PIL.Image` or tuple (pixels, width, height)
    :param return_position: A boolean that toggles between the return of QR-Code data or its position.
    :return: Returns the encoded data from the QR-Code or its position in the frame.
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


def calc_current_time_code(current_frame: int, frame_rate: float):
    total_time_in_milliseconds = ((current_frame - 1) / frame_rate) * 1000
    hour = total_time_in_milliseconds / (3600 * 1000)
    total_time_in_milliseconds %= (3600 * 1000)
    minutes = total_time_in_milliseconds / (60 * 1000)
    total_time_in_milliseconds %= (60 * 1000)
    seconds = total_time_in_milliseconds / 1000
    total_time_in_milliseconds %= 1000
    milliseconds = total_time_in_milliseconds
    time_code_position = ('%d:%d:%d:%d' % (hour, minutes, seconds, milliseconds))
    return time_code_position
