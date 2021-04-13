from tkinter import *
from audio_recorder import Recorder
from stmpy import Machine, Driver
from os import system
import os
import time

# TODO: Hans

class UIManager():

    def __init__(self, stm):
        self.stm
        self.setup()
    
    def setup(self):
        # create a tkinter window
        root = Tk()             
        
        # Open window having dimension 100x100
        root.geometry('100x100')
        
        # Create a Button
        start_btn = Button(root, text = 'Start', bd = '5',
                                command = self.on_start)

        stop_btn = Button(root, text = 'Stop', bd = '5',
        command = self.on_stop)
        
        # Set the position of button on the top of window.  
        start_btn.pack(side = 'top')
        stop_btn.pack(side = 'top')
        
        root.mainloop()
    
    def on_start(self):
        # TODO: Start recording
        pass
    def on_stop(self):
        # TODO: Stop recording
        pass


recorder = Recorder()


t0 = {'source': 'initial', 'target': 'ready'}
t1 = {'trigger': 'start', 'source': 'ready', 'target': 'recording'}
t2 = {'trigger': 'done', 'source': 'recording', 'target': 'processing'}
t3 = {'trigger': 'done', 'source': 'processing', 'target': 'ready'}

s_recording = {'name': 'recording', 'do': 'record()', "stop": "stop()"}
s_processing = {'name': 'processing', 'do': 'process()'}

stm = Machine(name='stm', transitions=[t0, t1, t2, t3], states=[s_recording, s_processing], obj=recorder)
recorder.stm = stm

driver = Driver()
driver.add_machine(stm)
driver.start()

ui_manager = UIManager(stm)
