import tkinter as tk
from stmpy import Driver
from audioPlayer import AudioPlayer
from audioRecorder import AudioRecorder
from pyaudio import PyAudio
from serverAPI import ServerAPI
from mqttAPI import MqttAPI
import sys
import logging


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self) -> None:
        self.lift()


class StartPage(Page):
    def __init__(self, main_view, ui_manager):
        self.ui_manager = ui_manager

        Page.__init__(self, main_view)
        #join_channel_input = tk.Entry(self)
        #join_channel_input.pack()
        #tk.Button(self, text="Join", command=lambda: self.join_channel(join_channel_input)).pack()
        tk.Button(self, text="Exit", command=ui_manager.exit).pack()

        label1 = tk.Label(self, text="Available channels")
        label1.config(font=("Courier", 16))
        label1.pack(side="top", fill="both", expand=True)

        for channel in self.ui_manager.serverAPI.getAvailableChannels():
            self.display_unsubscribed_channel(channel)
           
        label2 = tk.Label(self, text="Your channels")
        label2.config(font=("Courier", 16))
        label2.pack(side="top", fill="both", expand=True)

        for channel in self.ui_manager.serverAPI.get_channels():
            self.display_channel(channel)

    def display_unsubscribed_channel(self, channel : str) -> None:
        def subscribe():
            return self.join_channel(channel)

        container = tk.Frame(self, borderwidth=1, relief="groove")
        channel1 = tk.Label(container, text=channel)
        channel1.pack(side="left", fill="both", expand=True)
        tk.Button(container, text="Subscribe", command=subscribe).pack(side="left")
        container.pack(side="top", fill="both", expand=True)


    def display_channel(self, channel : str) -> None:
        def start_on_click():
             return self.start_recording(channel)

        def stop_on_click(): 
            return self.stop_recording(channel)

        frame = tk.Frame(self, borderwidth=1, relief="groove")
        tk.Label(frame, text=channel).pack(side="left", fill="both", expand=True)
        tk.Button(frame, text="Record", command=start_on_click).pack(side="left")
        tk.Button(frame, text="Stop", command=stop_on_click).pack(side="left")
        frame.pack(side="top", fill="both", expand=True)

    def start_recording(self, channel):
        self.ui_manager.recorder.start_recording(channel)

    def stop_recording(self, channel):
        self.ui_manager.recorder.state_machine.send("stop")

    """def join_channel(self, input: tk.Entry):
        channel = input.get()
        self.ui_manager.serverAPI.add_channel(channel)
        self.ui_manager.mqtt.update_subscriptions()
        self.display_channel(channel)"""

    def join_channel(self,channel):
        self.ui_manager.serverAPI.add_channel(channel)
        self.ui_manager.mqttAPI.update_subscriptions()
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
                 serverAPI: ServerAPI,
                 mqttAPI: MqttAPI
                 ):
        self.logger = logging.getLogger("WalkieTalkie")
        self.recorder = recorder
        self.driver = driver
        self.py_audio = py_audio
        self.serverAPI = serverAPI
        self.mqttAPI = mqttAPI
        self.setup()

    def setup(self) -> None:
        self.root = tk.Tk()
        main = MainView(self.root, self)
        main.pack(side="top", fill="both", expand=True)
        self.root.wm_geometry("300x600")
        self.root.mainloop()

    def exit(self) -> None:
        self.root.destroy()
        self.driver.stop()
        self.py_audio.terminate()
        sys.exit()
