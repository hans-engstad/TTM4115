from tkinter import *
from stmpy import Driver
from AudioPlayer import AudioPlayer
from AudioRecorder import AudioRecorder
from pyaudio import PyAudio
import sys

class UIManager():

    def __init__(self, recorder : AudioRecorder, driver : Driver, py_audio : PyAudio):
        self.recorder = recorder
        self.driver = driver
        self.py_audio = py_audio
        self.setup()


    def setup(self):
        # Create a tkinter window
        self.root = Tk()
        
        # Open window having dimension 200x200
        self.root.geometry('200x200')
        
        # Create a Button
        start_btn = Button(self.root, text = 'Start', bd = '5', command = self.recorder.start_recording)
        stop_btn = Button(self.root, text = 'Stop', bd = '5', command = self.recorder.stop_recording)

        queue_1_btn = Button(self.root, text = 'Exit', bd = '5', command = self.exit).pack()
        
        # Set the position of button on the top of window.  
        start_btn.pack(side = 'top')
        stop_btn.pack(side = 'top')
        
        # Start main loop of tkinter window
        self.root.mainloop()
    
    def exit(self):
        self.root.destroy()
        self.driver.stop()
        self.py_audio.terminate()
        sys.exit()

