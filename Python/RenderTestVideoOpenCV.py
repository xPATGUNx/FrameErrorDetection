import cv2 as cv
import numpy as np
import glob
import os
import time
from Python.QRCodeTools import generate_qr_codes


def render_test_video(*, video_file_path, new_video_file_name=None, codec=None, custom_frame_rate=None):
    try:
        cap = cv.VideoCapture(video_file_path)
        total_video_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        print('Total amount of Frames in video: ' + str(total_video_frames))
        if custom_frame_rate is None:
            fps = cap.get(cv.CAP_PROP_FPS)
        else:
            fps = custom_frame_rate

        generate_qr_codes(total_video_frames)
        frame_counter = 0
        img_array = []

        for qr_code_count in range(1, total_video_frames):
            path_to_qr_code = 'Images/QR_Code_Frame_' + str(qr_code_count) + '.png'
            # print(path_to_qr_code)
            img = cv.imread(path_to_qr_code)
            img_height, img_width, _ = img.shape
            img_array.append(img)

        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        base_name = os.path.basename(video_file_path)
        base_name = os.path.splitext(base_name)[0]
        if new_video_file_name is None:
            video_file_name = 'Video/QR_Code_Videos/' + base_name + ' ' + str(fps) + 'FPS ' \
                              + str(5000) + ' Frames.mp4'
        else:
            video_file_name = new_video_file_name

        if codec is not None:
            fourcc = codec
        else:
            codec_in_hex = hex(int(cap.get(cv.CAP_PROP_FOURCC)))[2:]
            codec_in_bytes = bytes.fromhex(codec_in_hex)
            codec_from_video = codec_in_bytes.decode("ASCII")
            fourcc = cv.VideoWriter_fourcc(*codec_from_video)

        video_size = (frame_width, frame_height)
        out = cv.VideoWriter(video_file_name, fourcc, fps, video_size)

        x_position = 0
        y_position = 0

        if not cap.isOpened():
            print("Error opening video stream or file")

        print('Beginning rendering process...')
        amount_of_frames = 0
        while frame_counter < 5000:

            ret, frame = cap.read()

            if ret:

                frame[y_position:y_position + img_height, x_position:x_position + img_width] = img_array[frame_counter]
                print(frame_counter)
                out.write(frame)
                # cv.imshow('Frame', frame)
                frame_counter += 1

            else:
                break

        cap.release()
        out.release()
        cv.destroyAllWindows()
        print('Video rendering complete.')
    finally:
        time.sleep(1)
        # delete_temp_images()


def delete_temp_images():
    print('Deleting temp files...')
    for filename in glob.glob('Images/*.png'):
        os.remove(filename)
    print('Deletion complete.')


if __name__ == '__main__':
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=24.0)
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=25.0)
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=29.97)
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=30.0)
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=50.0)
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=59.94)
    render_test_video(video_file_path='D:/Test Videos/Fractured 1080p.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'),
                      custom_frame_rate=60.0)

    # render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_25FPS_1080P.mp4',
    #                   new_video_file_name='Video/QR_150_Frames_25FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
    #
    # render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_29.97FPS_1080P.mp4',
    #                   new_video_file_name='Video/QR_150_Frames_29.97FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
    #
    # render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_30FPS_1080P.mp4',
    #                   new_video_file_name='Video/QR_150_Frames_30FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
    #
    # render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_50FPS_1080P.mp4',
    #                   new_video_file_name='Video/QR_150_Frames_50FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
    #
    # render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_59.97FPS_1080P.mp4',
    #                   new_video_file_name='Video/QR_150_Frames_59.97FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
    #
    # render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_60FPS_1080P.mp4',
    #                   new_video_file_name='Video/QR_150_Frames_60FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
