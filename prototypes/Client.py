from stmpy import Driver
import pyaudio
from AudioRecorder import AudioRecorder
from UIManager import UIManager
from AudioPlayer import AudioPlayer
from MQTT import MQTT
from ChannelManager import ChannelManager

# Instantiate third-party dependencies
py_audio = pyaudio.PyAudio()
driver = Driver()   # STMPY driver that will run all state machines

# Instantiate our classes
channel_manager = ChannelManager()
player = AudioPlayer(driver, py_audio)
mqtt = MQTT(player, channel_manager)
recorder = AudioRecorder(mqtt, driver, py_audio)

# Start state machine driver, state machines should have already been
# registered through dependency injection (Passed reference to driver
# into each state machine wrappers)
driver.start()

# Instantiate UIManager, which will render ui in a new window
ui_manager = UIManager(recorder, driver, py_audio, channel_manager)
