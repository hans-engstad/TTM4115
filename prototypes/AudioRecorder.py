import pyaudio
import wave

class AudioRecorder:
    def __init__(self, mqtt):
        self.recording = False
        self.fs = 44100  # Record at 44100 samples per second
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.filename = "output.wav"

        self.mqtt = mqtt
        
    def record(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.sample_format,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True)
        
        self.recording = True
        print("Recording audio")
        while self.recording:
            data = stream.read(self.chunk)
            self.mqtt.publish("insert_topic_here", data)
        
        print("Done recording audio")

        # Simulate that all packages are now recieved
        self.mqtt.simulate_recieve_buffer()

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        
    def stop(self):
        self.recording = False
