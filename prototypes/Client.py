from stmpy import Driver
import pyaudio
from AudioRecorder import AudioRecorder
from UIManager import UIManager
from MQTT import MQTT
from ChannelManager import ChannelManager
import logging

# Configure module wide logger
logger = logging.getLogger('WalkieTalkie')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(filename)s : [%(levelname)s] : %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Instantiate third-party dependencies
py_audio = pyaudio.PyAudio()
driver = Driver()   # STMPY driver that will run all state machines

# Instantiate our classes
channel_manager = ChannelManager()
mqtt = MQTT(driver, channel_manager, py_audio)
recorder = AudioRecorder(mqtt, driver, py_audio, channel_manager)

# Start state machine driver, state machines should have already been
# registered through dependency injection (Passed reference to driver
# into each state machine wrappers)
driver.start()

# Instantiate UIManager, which will render ui in a new window
ui_manager = UIManager(recorder, driver, py_audio, channel_manager, mqtt)

