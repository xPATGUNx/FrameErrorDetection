import cv2 as cv
import os
import subprocess
from QRCodeTools import generate_qr_codes, delete_generated_qr_codes


def render_test_video(path_to_video: str, *, frame_rate: float, qr_code_offset: int, format_profile: str = None,
                      format_level: str = None):
    total_amount_of_frames = get_total_amount_of_frames_from_video(path_to_video)
    amount_of_leading_zeros = len(str(total_amount_of_frames))
    base_name = os.path.basename(path_to_video)
    name_of_rendered_video = f'Rendered_Videos/qr_test_vid_{total_amount_of_frames}_frames_{frame_rate}fps_{base_name}'
    if os.path.exists(name_of_rendered_video):
        os.remove(name_of_rendered_video)

    delete_generated_qr_codes()
    generate_qr_codes(total_amount_of_frames)

    if format_profile and format_level is not None:
        ffmpeg_command = f'ffmpeg -r {frame_rate} -i {path_to_video} ' \
                         f'-r {frame_rate} -i Images/QR_Code_Frame_%0{amount_of_leading_zeros}d.png ' \
                         f'-filter_complex "[0:v][1:v] ' \
                         f'overlay={qr_code_offset}:{qr_code_offset}" ' \
                         f'-profile:v {format_profile} -level:v {format_level} ' \
                         f'{name_of_rendered_video} ' \
                         f'-vframes {total_amount_of_frames}'

        print(ffmpeg_command)
        pass_command(ffmpeg_command)

    else:
        ffmpeg_command = f'ffmpeg -r {frame_rate} -i {path_to_video} ' \
                         f'-r {frame_rate} -i Images/QR_Code_Frame_%0{amount_of_leading_zeros}d.png ' \
                         f'-filter_complex "[0:v][1:v] ' \
                         f'overlay={qr_code_offset}:{qr_code_offset}" {name_of_rendered_video} ' \
                         f'-vframes {total_amount_of_frames}'

        print(ffmpeg_command)
        pass_command(ffmpeg_command)


def pass_command(cmd_line: str):
    subprocess.check_output(cmd_line, shell=True)


def get_total_amount_of_frames_from_video(path_to_video: str):
    cap = cv.VideoCapture(path_to_video)
    total_amount_of_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    print(total_amount_of_frames)

    return total_amount_of_frames


if __name__ == '__main__':

    render_test_video('Video/Videos_in_different_Framerates/ft-60.mp4', frame_rate=60, qr_code_offset=20,
                      format_profile='main', format_level='4.0')
