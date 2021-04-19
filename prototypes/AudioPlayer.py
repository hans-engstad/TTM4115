# TODO: Signe
import pyaudio
from pyaudio import PyAudio
from stmpy import Machine, Driver


class AudioPlayer():

    def __init__(self,
                 driver: Driver,
                 py_audio: PyAudio
                 ):
        self.py_audio = py_audio
        self.state_machine = Machine(
            name="audio_machine",
            transitions=self._get_transitions(),
            states=self._get_states(),
            obj=self
        )
        driver.add_machine(self.state_machine)

    # Private methods

    def _get_transitions(self):
        return [
            {'source': 'initial', 'target': 'ready'},
            {'trigger': 'play', 'source': 'ready', 'target': 'playing',
                'effect': self._start_player.__name__},
            {'trigger': 'done', 'source': 'playing',
                'target': 'waiting_for_next_chunk'},
            {'trigger': 't', 'source': 'waiting_for_next_chunk',
                'target': 'ready', 'effect': self._stop_player.__name__},
            {'trigger': 'play', 'source': 'waiting_for_next_chunk',
                'target': 'playing', 'effect': 'stop_timer("t")'},
        ]

    def _get_states(self):
        return [
            {'name': 'ready'},
            {'name': 'playing', 'do': '_play(*)', 'play': 'defer'},
            {'name': 'waiting_for_next_chunk',
                'entry': 'start_timer("t", 1000)'},
        ]

    def _play(self, data):
        """
        Play given data
        """
        # Write to audio stream to play sound
        self.audio_stream.write(data)

    def _start_player(self):
        """
        Open stream that is used to play audio
        """
        print("Starting player")
        self.audio_stream = self.py_audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True
        )

    def _stop_player(self):
        """
        Close the stream used to play audio. 
        """
        print("Stopping player")
        self.audio_stream.stop_stream()
        self.audio_stream.close()

    # Public methods

    def play(self, data):
        """
        Play given audio data by sending it to the state machine. \n
        If the player is already playing something else, the data 
        will be queued and played at a later point using defer. 
        """
        self.state_machine.send("play", args=[data])
