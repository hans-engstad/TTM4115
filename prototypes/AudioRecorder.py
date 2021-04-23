from pyaudio import PyAudio
import pyaudio
import wave
from MQTT import MQTT
from stmpy import Driver, Machine
import json
import base64
import ChannelManager
import logging


class AudioRecorder:
    def __init__(self, mqtt: MQTT, driver: Driver, py_audio: PyAudio, channel_manager: ChannelManager):
        self.logger = logging.getLogger("WalkieTalkie")
        self.channel_manager = channel_manager

        # Define private variables
        self._recording = False

        # Save references
        self.mqtt = mqtt
        self.py_audio = py_audio

        # Create state machine
        self.state_machine = Machine(
            name="audio_recorder",
            transitions=self._get_transitions(),
            states=self._get_states(),
            obj=self
        )
        driver.add_machine(self.state_machine)

    def _record(self, channel):
        fs = 44100  # Record at 44100 samples per second
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2

        stream = self.py_audio.open(
            format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

        self._recording = True
        self.logger.info(f'Audio recording started for channel {channel}')
        while self._recording:
            payload = stream.read(chunk)
            encodedPayload = base64.b64encode(payload).decode('ascii')
            senderID = self.channel_manager.getUserID()

            packet = {
                "senderID": senderID,
                "payload": encodedPayload
            }

            encodedPacket = json.dumps(packet)
            self.mqtt.publish(channel, encodedPacket)

        self.logger.info(f"Audio recording stopped for channel {channel}")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

    def _get_states(self):
        return [
            {'name': 'ready'},
            {'name': 'recording',
                'do': '_record(*)', "stop": "stop_recording()"},
        ]

    def _get_transitions(self):
        return [
            {'source': 'initial', 'target': 'ready'},
            {'trigger': 'start_recording', 'source': 'ready', 'target': 'recording'},
            {'trigger': 'done', 'source': 'recording', 'target': 'ready'},
        ]

    def stop_recording(self):
        self._recording = False

    def start_recording(self, channel):
        self.state_machine.send("start_recording", args=[channel])
