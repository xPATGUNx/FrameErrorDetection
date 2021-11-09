import sys
import time
from Python.TestFullRangeFrameDrops import test_for_frame_errors
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QLabel, QComboBox,
                               QRadioButton, QCheckBox, QFileDialog)


# TODO: Add PyDoc
class UserInterface(QDialog):

    def __init__(self, parent=None):
        super(UserInterface, self).__init__(parent)
        # Create widgets
        self.test_run_name_label = QLabel('Name/Tag of test run:')
        self.test_run_name = QLineEdit('FED Test Run')

        self.report_path_label = QLabel('Path to report storage:')
        self.report_path = QLineEdit(r'D:\Reports')
        self.report_path_select_button = QPushButton('Select Directory')

        self.capture_path_label = QLabel('Path to video capture directory:')
        self.capture_path = QLineEdit(r'D:\Captured Video')
        self.capture_path_select_button = QPushButton('Select Directory')

        self.expected_frames_label = QLabel('Total amount of expected video frames:')
        self.expected_frames = QLineEdit('5000')

        self.recording_framerate_label = \
            QLabel('Capture framerate (to simulate a consumer display set this to \'60FPS\'):')
        self.recording_framerate = QComboBox()
        self.recording_framerate.addItems(['60FPS', '59.94FPS', '50FPS', '30FPS', '29.97FPS', '25FPS', '24FPS'])

        self.recording_device_label = QLabel('Recording Device:')
        self.recording_device_bmd = QRadioButton('Blackmagic Design Intensity Pro 4k')
        self.recording_device_bmd.toggled.connect(lambda: self.button_state(self.recording_device_bmd))
        self.recording_device_elgato = QRadioButton('Elgato Game Capture 4k60 Pro')
        self.recording_device_elgato.toggled.connect(lambda: self.button_state(self.recording_device_elgato))

        self.playback_frame_rate_label = QLabel('Framerate of video playback:')
        self.playback_frame_rate = QLineEdit('60')

        self.open_report_after_run_radio_button = QCheckBox('Open report after test run')

        self.button = QPushButton('Run Test')

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.test_run_name_label)
        layout.addWidget(self.test_run_name)
        layout.addWidget(self.report_path_label)
        layout.addWidget(self.report_path)
        layout.addWidget(self.report_path_select_button)
        layout.addWidget(self.capture_path_label)
        layout.addWidget(self.capture_path)
        layout.addWidget(self.capture_path_select_button)
        layout.addWidget(self.expected_frames_label)
        layout.addWidget(self.expected_frames)
        layout.addWidget(self.recording_framerate_label)
        layout.addWidget(self.recording_framerate)
        layout.addWidget(self.recording_device_label)
        layout.addWidget(self.recording_device_bmd)
        layout.addWidget(self.recording_device_elgato)
        layout.addWidget(self.playback_frame_rate_label)
        layout.addWidget(self.playback_frame_rate)
        layout.addWidget(self.open_report_after_run_radio_button)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)

        self.recording_device_bmd.setChecked(True)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.execute_test_run)
        self.report_path_select_button.clicked.connect(self.select_report_dir)
        self.capture_path_select_button.clicked.connect(self.select_capture_dir)

    # Greets the user
    def execute_test_run(self):
        if self.recording_device_bmd.isChecked() is False and self.recording_device_elgato.isChecked() is False:
            print('No capture device has been selected. Please select one to execute the test.')

        else:
            timestr: str = time.strftime("%Y %m %d-%H%M%S")
            test_name = f'{self.test_run_name.text()} {timestr}'
            print(f'Name/Tag of test run: {test_name}')
            path_to_report_storage = self.report_path.text()
            print(f'Path to report storage: {path_to_report_storage}')
            capture_path = self.capture_path.text()
            print(f'Capture path: {capture_path}')
            expected_frames = int(self.expected_frames.text())
            print(f'Exptected amount of Frames: {expected_frames}')
            recording_frame_rate = self.recording_framerate.currentText()
            print(f'Recording frame rate: {recording_frame_rate} FPS')
            playback_frame_rate = int(self.playback_frame_rate.text())
            print(f'Playback frame rate: {playback_frame_rate}')

            if self.open_report_after_run_radio_button.isChecked() is True:
                open_report = True
            else:
                open_report = False

            if self.recording_device_bmd.isChecked() is True:
                print(f'Selected recording device: {self.recording_device_bmd.text()}')
                recording_scene = f'BMD {playback_frame_rate} FPS'
            if self.recording_device_elgato.isChecked() is True:
                print(f'Selected recording device: {self.recording_device_elgato.text()}')
                recording_scene = f'Elgato {playback_frame_rate} FPS'

            additional_recording_time = 15
            recording_length = int(expected_frames / playback_frame_rate + additional_recording_time)

            test_for_frame_errors(name_of_test_run=test_name,
                                  video_directory_path=capture_path,
                                  expected_amount_of_frames=expected_frames,
                                  recording_frame_rate=recording_frame_rate,
                                  recording_scene=recording_scene,
                                  playback_frame_rate=playback_frame_rate,
                                  recording_length=recording_length,
                                  open_report=open_report,
                                  report_path=path_to_report_storage)

            print('Test run completed.')

    def select_report_dir(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.report_path.setText(directory)

    def select_capture_dir(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.capture_path.setText(directory)

    def button_state(self, button):
        if button.text() == 'Blackmagic Design Intensity Pro 4k':
            if button.isChecked():
                self.recording_device_elgato.setChecked(False)
        elif button.text() == 'Elgato Game Capture 4k60 Pro':
            if button.isChecked():
                self.recording_device_bmd.setChecked(False)
