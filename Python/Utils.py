

def calc_current_time_code(current_frame: int, frame_rate: float):
    """
    Function to calculate time code from current frame.
    :param current_frame: Current frame as an int value.
    :param frame_rate: Playback frame rate as an int value.
    :return: returns a time code string in 'hours:minutes:seconds:milliseconds'.
    """
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
