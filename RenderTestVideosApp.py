import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QFileDialog)
from Python.RenderTestVideoFFMPEG import render_test_video


class VideoRenderUI(QDialog):

    def __init__(self, parent=None):
        super(VideoRenderUI, self).__init__(parent)
        # Create widgets
        note = '(note: the path string is not allowed to contain blank spaces!)'
        self.path_to_video_label = QLabel(f'Enter path to video {note}:')
        self.path_to_video = QLineEdit()
        self.report_file_select_button = QPushButton('Select File')

        self.frame_rate_label = QLabel('Set video frame rate:')
        self.frame_rate = QLineEdit('60')

        self.qr_offset_label = QLabel('Offset of QR code location:')
        self.qr_offset = QLineEdit('20')

        self.button = QPushButton('Render Video!')

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.path_to_video_label)
        layout.addWidget(self.path_to_video)
        layout.addWidget(self.report_file_select_button)
        layout.addWidget(self.frame_rate_label)
        layout.addWidget(self.frame_rate)
        layout.addWidget(self.qr_offset_label)
        layout.addWidget(self.qr_offset)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.execute_video_render)
        self.report_file_select_button.clicked.connect(self.select_file)

    def execute_video_render(self):

        video_path = self.path_to_video.text()
        frame_rate = self.frame_rate.text()
        qr_code_offset = self.qr_offset.text()
        render_test_video(path_to_video=video_path, frame_rate=frame_rate, qr_code_offset=qr_code_offset)

    def select_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        directory = dialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='*.mp4')
        self.path_to_video.setText(str(directory[0]))


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    ui = VideoRenderUI()
    ui.show()
    # Run the main Qt loop
    sys.exit(app.exec())
