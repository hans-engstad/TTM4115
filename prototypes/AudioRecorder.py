from pyaudio import PyAudio
import pyaudio
import wave
from mqttAPI import MqttAPI
from stmpy import Driver, Machine
import json
import base64
from serverAPI import ServerAPI
import logging
from packet import Packet


class AudioRecorder:
    def __init__(self, mqttAPI: MqttAPI, driver: Driver, py_audio: PyAudio, serverAPI: ServerAPI):
        self.logger = logging.getLogger("WalkieTalkie")
        self.serverAPI = serverAPI

        # Define private variables
        self._recording = False

        # Save references
        self.mqttAPI = mqttAPI
        self.py_audio = py_audio

        # Create state machine
        self.state_machine = Machine(
            name="audio_recorder",
            transitions=self._get_transitions(),
            states=self._get_states(),
            obj=self
        )
        driver.add_machine(self.state_machine)

    def _record(self, channel) -> None:
        fs = 44100  # Record at 44100 samples per second
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2

        stream = self.py_audio.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

        self._recording = True
        self.logger.info(f'Audio recording started for channel {channel}')
        while self._recording:
            senderID = self.serverAPI.getUserID()
            priority = self.serverAPI.getChannelPriority(channel)
            message = stream.read(chunk)
            encodedMessage = base64.b64encode(message).decode('ascii')
            packet = Packet(priority, channel, senderID, encodedMessage)
            self.mqttAPI.publish(packet)

        self.logger.info(f"Audio recording stopped for channel {channel}")
        stream.stop_stream()
        stream.close()

    def _get_states(self) -> list:
        return [
            {'name': 'ready'},
            {'name': 'recording',
            'do': '_record(*)', "stop": "stop_recording()"},
        ]

    def _get_transitions(self) -> list:
        return [
            {'source': 'initial', 'target': 'ready'},
            {'trigger': 'start_recording', 'source': 'ready', 'target': 'recording'},
            {'trigger': 'done', 'source': 'recording', 'target': 'ready'},
        ]

    def stop_recording(self) -> None:
        self._recording = False

    def start_recording(self, channel) -> None:
        self.state_machine.send("start_recording", args=[channel])
