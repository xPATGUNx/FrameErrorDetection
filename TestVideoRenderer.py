import cv2 as cv
import numpy as np
import glob
import os
import time
from QRCodeGenerator import QRCodeGenerator


def render_test_video(*, video_file_path, new_video_file_name, codec=None):
    try:
        cap = cv.VideoCapture(video_file_path)
        total_video_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        framerate = cap.get(cv.CAP_PROP_FPS)
        gen = QRCodeGenerator(total_video_frames)
        gen.generate_qr_codes()
        frame_counter = 0
        img_array = []

        for filename in glob.glob('Images/*.png'):
            img = cv.imread(filename)
            img_height, img_width, _ = img.shape
            img_array.append(img)

        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        video_filename = new_video_file_name

        if codec is not None:
            fourcc = codec
        else:
            codec_in_hex = hex(int(cap.get(cv.CAP_PROP_FOURCC)))[2:]
            codec_in_bytes = bytes.fromhex(codec_in_hex)
            codec_from_video = codec_in_bytes.decode("ASCII")
            fourcc = cv.VideoWriter_fourcc(*codec_from_video)

        fps = framerate
        video_size = (frame_width, frame_height)
        out = cv.VideoWriter(video_filename, fourcc, fps, video_size)

        x_position = 0
        y_position = 0

        if not cap.isOpened():
            print("Error opening video stream or file")

        print('Beginning rendering process...')
        while cap.isOpened():

            ret, frame = cap.read()

            if ret:

                frame[y_position:y_position + img_height, x_position:x_position + img_width] = img_array[frame_counter]

                out.write(frame)
                # cv.imshow('Frame', frame)
                frame_counter += 1
                if cv.waitKey(25) & 0xFF == ord('q'):
                    break

            else:
                break

        cap.release()
        out.release()
        cv.destroyAllWindows()
        print('Video rendering complete.')
    finally:
        time.sleep(1)
        delete_temp_images()


def delete_temp_images():
    print('Deleting temp files...')
    for filename in glob.glob('Images/*.png'):
        os.remove(filename)
    print('Deletion complete.')


if __name__ == '__main__':
    render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_24FPS_1080P.mp4',
                      new_video_file_name='Video/QR_150_Frames_24FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))

    render_test_video(video_file_path='Video/Initial Test Video/RW_150Frames_25FPS_1080P.mp4',
                      new_video_file_name='Video/QR_150_Frames_25FPS.mp4', codec=cv.VideoWriter_fourcc(*'mp4v'))
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
