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
        self.p = pyaudio.PyAudio() 

        self.mqtt = mqtt
        
    def record(self):
        stream = self.p.open(format=self.sample_format,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True)
        self.frames = []  # Initialize array to store frames
        # Store data in chunks for 3 seconds
        self.recording = True
        while self.recording:
            data = stream.read(self.chunk)
            self.mqtt.publish("insert_topic_here", data)
            # self.frames.append(data)
        print("done recording")

        # Simulate that all packages are now recieved
        self.mqtt.simulate_recieve_buffer()

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        
    def stop(self):
        print("stop")
        self.recording = False
    
    def process(self):
        print("processing")
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
