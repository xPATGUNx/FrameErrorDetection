import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QFileDialog, QFrame,
                               QComboBox)
from Python.RenderTestVideoFFMPEG import render_test_video, render_qr_code_clip


class VideoRenderUI(QDialog):
    """
    A PyQT based class to build the user interface for test video rendering.
    """
    def __init__(self, parent=None):
        super(VideoRenderUI, self).__init__(parent)
        # Create widgets
        self.render_video_label = QLabel(f'Render Test Video')
        self.path_to_video_label = QLabel(f'Enter path to video:')
        self.path_to_video = QLineEdit()
        self.report_file_select_button = QPushButton('Select File')

        self.frame_rate_label = QLabel('Set video frame rate:')
        self.frame_rate = QLineEdit('60')

        self.qr_offset_label = QLabel('Offset of QR code location:')
        self.qr_offset = QLineEdit('20')

        self.start_render_button = QPushButton('Render Video!')

        self.render_qr_clip_label = QLabel('Render QR Code Clip')
        self.video_title_label = QLabel('Enter video title:')
        self.video_title = QLineEdit('QR Code Video Clip')
        self.save_path_label = QLabel('Enter save location:')
        self.save_path = QLineEdit(r'D:/Test Videos')
        self.save_path_select_button = QPushButton('Select File')

        self.qr_frame_rate_label = QLabel('Framerate of clip:')
        self.qr_frame_rate = QComboBox()
        self.qr_frame_rate.addItems(['60', '59.94', '50', '30', '29.97', '25', '24'])

        self.amount_of_frames_label = QLabel('Amount of video frames:')
        self.amount_of_frames = QLineEdit('5000')

        self.qr_render_button = QPushButton('Render QR Code Clip!')

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.render_video_label)
        layout.addWidget(QHLine())
        layout.addWidget(self.path_to_video_label)
        layout.addWidget(self.path_to_video)
        layout.addWidget(self.report_file_select_button)
        layout.addWidget(self.frame_rate_label)
        layout.addWidget(self.frame_rate)
        layout.addWidget(self.qr_offset_label)
        layout.addWidget(self.qr_offset)
        layout.addWidget(self.start_render_button)
        layout.addWidget(QHLine())
        layout.addWidget(QHLine())
        layout.addWidget(self.render_qr_clip_label)
        layout.addWidget(QHLine())
        layout.addWidget(self.video_title_label)
        layout.addWidget(self.video_title)
        layout.addWidget(self.save_path_label)
        layout.addWidget(self.save_path)
        layout.addWidget(self.save_path_select_button)
        layout.addWidget(self.qr_frame_rate_label)
        layout.addWidget(self.qr_frame_rate)
        layout.addWidget(self.amount_of_frames_label)
        layout.addWidget(self.amount_of_frames)
        layout.addWidget(self.qr_render_button)

        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.start_render_button.clicked.connect(self.execute_video_render)
        self.report_file_select_button.clicked.connect(self.select_file)
        self.save_path_select_button.clicked.connect(self.select_dir)
        self.qr_render_button.clicked.connect(self.execute_qr_code_clip_render)

    def execute_video_render(self):
        """
        Executes the video render process.
        """
        video_path = self.path_to_video.text()
        frame_rate = self.frame_rate.text()
        qr_code_offset = self.qr_offset.text()
        render_test_video(path_to_video=video_path, frame_rate=frame_rate, qr_code_offset=qr_code_offset)

    def execute_qr_code_clip_render(self):
        video_title = self.video_title.text()
        save_path = self.save_path.text() + '/' + video_title + '.mp4'
        frame_rate = float(self.qr_frame_rate.currentText())
        total_frames = int(self.amount_of_frames.text())
        render_qr_code_clip(path_to_video=save_path, frame_rate=frame_rate, total_amount_of_frames=total_frames)

    def select_file(self):
        """
        Triggers a select file system dialog.
        """
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        directory = dialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='*.mp4')
        self.path_to_video.setText(str(directory[0]))

    def select_dir(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.save_path.setText(directory)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = VideoRenderUI()
    ui.show()
    sys.exit(app.exec())
