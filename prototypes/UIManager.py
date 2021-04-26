import tkinter as tk
from stmpy import Driver
from AudioPlayer import AudioPlayer
from AudioRecorder import AudioRecorder
from pyaudio import PyAudio
from ChannelManager import ChannelManager
from MQTT import MQTT
import sys
import logging


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class StartPage(Page):
    def __init__(self, main_view, ui_manager):
        self.ui_manager = ui_manager
        self.logger = logging.getLogger("WalkieTalkie")
        Page.__init__(self, main_view)
        join_channel_input = tk.Entry(self)
        join_channel_input.pack()
        tk.Button(self, text="Join", command=lambda: self.join_channel(
            join_channel_input)).pack()
        tk.Button(self, text="Exit", command=ui_manager.exit).pack()

        label1 = tk.Label(self, text="Available channels")
        label1.config(font=("Courier", 24))
        label1.pack(side="top", fill="both", expand=True)
        for channel in self.ui_manager.channel_manager.getAvailableChannels():
            channel1 = tk.Label(self, text=channel)
            channel1.pack(side="top", fill="both", expand=True)

        label2 = tk.Label(self, text="Your channels")
        label2.config(font=("Courier", 24))
        label2.pack(side="top", fill="both", expand=True)

        for channel in self.ui_manager.channel_manager.get_channels():
            self.display_channel(channel)

    def display_channel(self, channel):
        frame = tk.Frame(self, borderwidth=1)
        tk.Label(frame, text=channel).pack(
            side="top", fill="both", expand=True)

        def start_on_click(): return self.start_recording(channel)
        def stop_on_click(): return self.stop_recording(channel)
        tk.Button(frame, text="Record", command=start_on_click).pack()
        tk.Button(frame, text="Stop", command=stop_on_click).pack()

        frame.pack(side="top", fill="both", expand=True)

    def start_recording(self, channel):
        self.ui_manager.recorder.start_recording(channel)

    def stop_recording(self, channel):
        self.ui_manager.recorder.state_machine.send("stop")

    def join_channel(self, input: tk.Entry):
        channel = input.get()
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
                 recorder: AudioRecorder,
                 driver: Driver,
                 py_audio: PyAudio,
                 channel_manager: ChannelManager,
                 mqtt: MQTT
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
