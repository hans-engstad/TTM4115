from stmpy import Driver
import pyaudio
from audioRecorder import AudioRecorder
from UIManager import UIManager
from mqttAPI import MqttAPI
from serverAPI import ServerAPI
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
pyAudio = pyaudio.PyAudio()
driver = Driver()   # STMPY driver that will run all state machines

# Instantiate our classes
serverAPI = ServerAPI()
mqttAPI = MqttAPI(driver, serverAPI, pyAudio)
recorder = AudioRecorder(mqttAPI, driver, pyAudio, serverAPI)

# Start state machine driver, state machines should have already been
# registered through dependency injection (Passed reference to driver
# into each state machine wrappers)
driver.start()

# Render GUI in a new window
ui_manager = UIManager(recorder, driver, pyAudio, serverAPI, mqttAPI)

