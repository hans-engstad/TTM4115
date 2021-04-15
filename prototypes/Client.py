from stmpy import Driver
import pyaudio
from AudioRecorder import AudioRecorder
from ClientMachine import ClientMachine
from UIManager import UIManager
from AudioPlayer import AudioPlayer
from MQTT import MQTT


# Instantiate third-party dependencies
py_audio = pyaudio.PyAudio()
driver = Driver()   # STMPY driver that will run all state machines

# Instantiate our classes
player = AudioPlayer(driver, py_audio)
mqtt = MQTT(player)
recorder = AudioRecorder(mqtt)
client_machine = ClientMachine(driver, recorder, player, mqtt)

# Start state machine driver, state machines should have already been 
# registered through dependency injection (Passed reference to driver 
# into each state machine wrappers)
driver.start()

# Instantiate UIManager, which will render ui in a new window

ui_manager = UIManager(client_machine, driver, py_audio)
