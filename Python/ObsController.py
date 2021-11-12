import obswebsocket.exceptions
from obswebsocket import obsws, requests
import time


class ObsController:
    """
    API Class to easily control OBS (Open Broadcaster Studio) via obs-websocket.py.
    Visit https://obsproject.com/ to learn more about OBS.
    """
    def __init__(self, host='localhost', port=4444, password='Steinberg'):
        """
        Construct a new ObsController.
        :param host: Hostname to connect to
        :param port: TCP Port to connect to (Default is 4444)
        :param password: Password for the websocket server (Leave this field
            empty if no auth enabled on the server)
        """
        self.host = host
        self.port = port
        self.password = password
        self.web_socket = obsws(self.host, self.port, self.password)

    def connect_with_obs(self):
        """
        A function to connect with the OBS socket server.
        """
        try:
            self.web_socket.connect()
        except obswebsocket.exceptions.ConnectionFailure:
            print('Failed to connect with OBS. Please restart the OBS-Websocket server.')

    def disconnect_with_obs(self):
        """
        A function to disconnect with the OBS socket server.
        """
        self.web_socket.disconnect()

    def record(self, record_duration: int):
        """
        A function to trigger recording in OBS.
        :param record_duration: an integer that specifies the duration of recording in seconds.
        """
        self.web_socket.call(requests.StartRecording())
        print('Start of recording.')
        time.sleep(record_duration)
        self.web_socket.call(requests.StopRecording())
        print('End of recording.')

    def change_scene(self, name_of_scene: str):
        """
        Call this function to change the scene in OBS.
        :param name_of_scene: A string containing the exact name of the scene you want to change to.
        """
        self.web_socket.call(requests.SetCurrentSceneCollection(sc_name=name_of_scene))

    def set_profile(self, profile_name):
        """
        Call this function to change the current recoding profile in OBS.
        :param profile_name: A string containing the exact name of the profile you want to change to.
        """
        self.web_socket.call(requests.SetCurrentProfile(profile_name))

    def set_video_directory(self, *, path):
        """
        Call this function to set the directory where recorded videos will be stored.
        :param path: A string containing the path to the directory of desired video storage.
        """
        self.web_socket.call(requests.SetRecordingFolder(path))
