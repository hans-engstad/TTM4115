# TODO: Signe
import pyaudio
import wave
import os

from stmpy import Machine, Driver

class AudioPlayer():

    def __init__(self, driver, py_audio):
        self.py_audio = py_audio
        self.state_machine = Machine(
            name="audio_machine", 
            transitions=self._get_transitions(), 
            states=self._get_states(), 
            obj=self
        )
        driver.add_machine(self.state_machine)

    def play(self, data):
        """
        Play all given data
        """
        print("Starting to play audio")
        # open stream
        stream = self.py_audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True
        )

        # Play stream
        stream.write(data)

        # Stop stream
        stream.stop_stream()
        stream.close()


    def _get_transitions(self):
        return [
            {'source': 'initial', 'target': 'ready'},
            {'trigger': 'play', 'source': 'ready', 'target': 'playing'},
            {'trigger': 'done', 'source': 'playing', 'target': 'ready'},
        ]
    
    def _get_states(self):
        return [
            {'name': 'ready'},
            {'name': 'playing', 'do': 'play(*)', 'play': 'defer'},
        ]
    


    
        

    


        


