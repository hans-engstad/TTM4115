import tkinter as tk
from stmpy import Driver
from AudioPlayer import AudioPlayer
from AudioRecorder import AudioRecorder
from pyaudio import PyAudio
from ChannelManager import ChannelManager
from MQTT import MQTT
import sys

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class StartPage(Page):
    def __init__(self, main_view, ui_manager):
        self.ui_manager = ui_manager

        Page.__init__(self, main_view)
        join_channel_input = tk.Entry(self)
        join_channel_input.pack()
        join_button = tk.Button(self, text="Join", command = lambda: self.join_channel(join_channel_input)).pack()
        join_button = tk.Button(self, text="Exit", command = ui_manager.exit).pack()
        
        label = tk.Label(self, text="Your channels")
        label.config(font=("Courier", 44))

        label.pack(side="top", fill="both", expand=True)

        for channel in self.ui_manager.channel_manager.get_channels():
            self.display_channel(channel)
    
    def display_channel(self, channel):
        frame = tk.Frame(self, borderwidth=1)
        tk.Label(frame, text=channel).pack(side="top", fill="both", expand=True)
        start_on_click = lambda: self.start_recording(channel)
        stop_on_click = lambda: self.stop_recording(channel)
        tk.Button(frame, text="Record", command = start_on_click).pack()
        tk.Button(frame, text="Stop", command = stop_on_click).pack()

        frame.pack(side="top", fill="both", expand=True)

    def start_recording(self, channel):
        print("Start recording for channel: " + channel)
        self.ui_manager.recorder.start_recording(channel)

    def stop_recording(self, channel):
        print("Stop recording for channel: " + channel)
        self.ui_manager.recorder.stop_recording()

    def join_channel(self, input : tk.Entry):
        channel = input.get()
        print("Join channel: " + channel)
        self.ui_manager.channel_manager.add_channel(channel)
        self.ui_manager.mqtt.update_subscriptions()
        self.display_channel(channel)

    


class MainView(tk.Frame):
    def __init__(self, root, ui_manager):
        tk.Frame.__init__(self, root)
        start_page = StartPage(self, ui_manager=ui_manager)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        start_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        start_page.show()

class UIManager():

    def __init__(self, 
        recorder : AudioRecorder, 
        driver : Driver, 
        py_audio : PyAudio, 
        channel_manager : ChannelManager,
        mqtt : MQTT
    ):
        self.recorder = recorder
        self.driver = driver
        self.py_audio = py_audio
        self.channel_manager = channel_manager
        self.mqtt = mqtt
        self.setup()

    def setup(self):
        self.root = tk.Tk()
        main = MainView(self.root, self)
        main.pack(side="top", fill="both", expand=True)
        self.root.wm_geometry("500x400")
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        self.driver.stop()
        self.py_audio.terminate()
        sys.exit()

