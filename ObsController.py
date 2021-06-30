from obswebsocket import obsws, requests, events
import time


class ObsController:
    def __init__(self, host='localhost', port=4444, password='Steinberg'):
        self.host = host
        self.port = port
        self.password = password
        self.web_socket = obsws(self.host, self.port, self.password)

    def connect_with_obs(self):
        self.web_socket.connect()

    def disconnect_with_obs(self):
        self.web_socket.disconnect()

    def record(self, record_duration):
        self.web_socket.call(requests.StartRecording())
        print('Start of recording.')
        time.sleep(record_duration)
        self.web_socket.call(requests.StopRecording())
        print('End of recording.')

    def change_scene(self, name_of_scene):
        self.web_socket.call(requests.SetCurrentScene(scene_name=name_of_scene))

    def set_profile(self, profile_name):
        self.web_socket.call(requests.SetCurrentProfile(profile_name))

    def set_video_directory(self, *, path):
        self.web_socket.call(requests.SetRecordingFolder(path))
