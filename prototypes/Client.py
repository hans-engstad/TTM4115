from AudioRecorder import AudioRecorder
from ClientMachine import ClientMachine
from UIManager import UIManager
from AudioPlayer import AudioPlayer
from MQTT import MQTT
from stmpy import Driver

# Create STMPY driver that will run all state machines
driver = Driver()

player = AudioPlayer(driver)

mqtt = MQTT(player)
# Create recorder for recording audio
recorder = AudioRecorder(mqtt)

# TODO: Instantiate real implementation of AudioPlayer and MQTT

# Create ClientMachine, which is where the state machine lives
client_machine = ClientMachine(driver, recorder, player, mqtt)

# Start state machine driver, state machines should have already been 
# registered through dependency injection (Passed reference to driver 
# into each state machine wrappers)
driver.start()

# client_machine.state_machine.send()

# Instantiate UIManager, which will render ui in a new window
ui_manager = UIManager(client_machine)
