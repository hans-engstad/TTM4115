# TODO: Signe
import pyaudio
import wave
import os

from stmpy import Machine, Driver

class AudioPlayer():

    def __init__(self, driver):
        self.queue = ["sound1.wav", "sound2.wav"]     # Queue of files that are waiting to be played
        self.state_machine = Machine(
            name="audio_machine", 
            transitions=self._get_transitions(), 
            states=self._get_states(), 
            obj=self
        )
        driver.add_machine(self.state_machine)

    def play(self, data):
        """
        Play all items that are in the queue
        """
        if self._queue_empty():
            print("Nothing to play, queue is empty")
            return


        # Create an interface to PortAudio
        port_audio = pyaudio.PyAudio()

        # open stream
        stream = port_audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True
        )

        data = self.queue.j

        # Play chunk from queue as long as there are items there
        while(not self._queue_empty()):
            # Pop the first item of the queue
            data = self.queue.pop(0)

            # Play stream
            stream.write(data)
        

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        port_audio.terminate()

        
    
    def dequeue(self):
        if self._queue_empty():
            # Queue is empty, do nothing
            return
        
        # The queue has items, send play signal to state machine to trigger playing of queue
        self.state_machine.send("play")

    

    def queue_file(self, file_path):
        print("Start queue file")
        print("Queue file: " + file_path)
        self.queue.append(file_path)

    def _get_transitions(self):
        return [
            {'source': 'initial', 'target': 'ready'},
            {'trigger': 'play', 'source': 'ready', 'target': 'playing'},
            {'trigger': 'done', 'source': 'playing', 'target': 'ready'},
            {'trigger': 'queue', 'source': 'ready', 'target': 'ready', 'effect': 'queue_file(*)'}     # queue(*) will pass any arguments(and kwargs) to the method
            # {'trigger': 'new_file', 'source': 'playing', 'target': 'playing', 'effect': 'queue(*)'}
        ]
    
    def _get_states(self):
        return [
            {'name': 'ready', 'entry': 'dequeue'},
            # {'name': 'playing', 'do': 'play'},
            {'name': 'playing', 'do': 'play', 'queue': 'defer'},
            # {'name': 'recording', 'do': 'record()', "stop": "stop_recording()"},
            # {'name': 'processing', 'do': 'process()'}
        ]

    def _queue_empty(self):
        return len(self.queue) == 0
    

    def _play_file(self, data):
        """
        Play audio from binary data using PortAudio. 
        """

        print("Starting play file")

        # Create an interface to PortAudio
        port_audio = pyaudio.PyAudio()

        print("Opening stream")

        # open stream
        stream = port_audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True
        )

        print("Play stream")
        
        # Play stream
        stream.write(data)

        print("Stop stream")

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        port_audio.terminate()

    '''
    def _play_file(self, file_path):
        """
        Play audio file at given file_path using PortAudio. 
        """
        if not os.path.exists(file_path):
            print("ERROR: Can't play audio file becuase it does not exist (" + str(file_path) + ")")
            return

        # Open file
        wave_file = wave.open(file_path, 'rb')

        # Create an interface to PortAudio
        port_audio = pyaudio.PyAudio()

        # open stream
        stream = port_audio.open(format=port_audio.get_format_from_width(wave_file.getsampwidth()),
                channels=wave_file.getnchannels(),
                rate=wave_file.getframerate(),
                output=True)
        
        # Set chunk size of 1024 samples per data frame
        chunk = 1024

        # Read data
        data = wave_file.readframes(chunk)

        # Play stream
        while len(data) > 0:
            stream.write(data)
            data = wave_file.readframes(chunk)

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        port_audio.terminate()
    '''

    
        

    


        


