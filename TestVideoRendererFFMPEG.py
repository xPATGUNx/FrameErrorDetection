import os
import subprocess
from QRCodeTools import generate_qr_codes, delete_generated_qr_codes


def pass_command(cmd_line: str):
    subprocess.check_output(cmd_line, shell=True)

# ffmpeg -framerate 60 -i testvid.mp4 -i QR_Code_Frame_%04d.png -filter_complex "[0:v][1:v] overlay=20:20" test.mp4


def render_test_video(path_to_video: str, frame_rate: float, total_amount_of_frames: int, qr_code_offset: int):
    amount_of_leading_zeros = len(str(total_amount_of_frames))
    base_name = os.path.basename(path_to_video)
    name_of_rendered_video = f'Rendered_Videos/qr_test_vid_{total_amount_of_frames}_frames_{frame_rate}fps_{base_name}'
    if os.path.exists(name_of_rendered_video):
        os.remove(name_of_rendered_video)

    delete_generated_qr_codes()
    generate_qr_codes(total_amount_of_frames)

    ffmpeg_command = f'ffmpeg -r {frame_rate} -i {path_to_video} ' \
                     f'-r {frame_rate} -i Images/QR_Code_Frame_%0{amount_of_leading_zeros}d.png ' \
                     f'-filter_complex "[0:v][1:v] ' \
                     f'overlay={qr_code_offset}:{qr_code_offset}" {name_of_rendered_video} ' \
                     f'-vframes {total_amount_of_frames}'

    print(ffmpeg_command)
    pass_command(ffmpeg_command)

    while True:
        if os.path.exists(name_of_rendered_video):
            break
    delete_generated_qr_codes()


render_test_video('Video/QR_Code_Videos/QR_150_Frames_50FPS.mp4', 50, 300, 20)
