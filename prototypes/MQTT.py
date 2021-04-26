import paho.mqtt.client as mqtt
import logging
from AudioPlayer import AudioPlayer
from ChannelManager import ChannelManager
import json
import logging
from AudioPlayer import AudioPlayer
from stmpy import Machine, Driver
from pyaudio import PyAudio
from packet import Packet

class MQTT():

    def __init__(self, driver : Driver, channel_manager : ChannelManager, py_audio : PyAudio):
        self.logger = logging.getLogger("WalkieTalkie")
        self.players = {}  # userID -> audio player object
        self.channel_manager = channel_manager
        self.driver = driver
        self.py_audio = py_audio
        self.queue = []
        self.max_current_priority = -1

        MQTT_BROKER = 'mqtt.item.ntnu.no'
        MQTT_PORT = 1883
 
        # create client
        self.logger.info(f'Connecting to MQTT broker {MQTT_BROKER} at port {MQTT_PORT}')
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        self.mqtt_client.loop_start()
        self.update_subscriptions() 

        # Create state machine
        self.state_machine = Machine(
            name="mqtt",
            transitions=self._get_transitions(),
            states=self._get_states(),
            obj=self
        )
        driver.add_machine(self.state_machine)

    def _get_states(self):
        return [
            {'name': 'ready'},
            {'name': 'prioritising',
                'do': 'remove_low_priority_items()', 
                'receive': 'defer'
            },
            {'name':'sending',
                'do':'send_queue_to_player()',
                'receive': 'defer'
            }
        ]

    def _get_transitions(self):
        return [
            {'source': 'initial', 'target': 'ready','effect':'start_timer("t",300)'},
            {'trigger': 'receive', 'source': 'ready', 'target': 'ready', 'effect':'add_to_queue(*)'},
            {'trigger': 't', 'source': 'ready', 'target': 'prioritising'},
            {'trigger':'done','source':'prioritising','target':'sending'},
            {'trigger':'done','source':'sending','target':'ready','effect':'start_timer("t",300)'},
        ]

    def add_to_queue(self, packet : Packet):
        self.max_current_priority = max(self.max_current_priority, packet.priority)
        self.queue.append(packet)
       
    def remove_low_priority_items(self):
        new_queue = []

        for packet in self.queue:
            if packet.priority >= self.max_current_priority:
                new_queue.append(packet)
        
        self.queue = new_queue

    def send_queue_to_player(self):
        for packet in self.queue:
            if packet.senderID != self.channel_manager.getUserID():
                if packet.senderID not in self.players:
                    newPlayer = self.getNewPlayer()
                    self.players[packet.senderID] = newPlayer

                decoded_message = packet.get_decoded_message()
                self.players[packet.senderID].play(decoded_message)

        self.queue = []
        self.max_current_priority = -1

    def getNewPlayer(self):
        return AudioPlayer(self.driver, self.py_audio)

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self.logger.info(f'Successfully connected to MQTT broker')

    def on_message(self, client, userdata, msg):
        packet = Packet.deserialize(msg.payload)
        self.state_machine.send('receive',args=[packet])
        self.logger.debug(f'Incoming message to topic {packet.channel}')

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

    def update_subscriptions(self):
        """
        Sync subscribed topics with channel manager
        """
        # Unsubscribe to all channels
        self.mqtt_client.unsubscribe("#")

        # Resubscribe to updated channels list
        for channel in self.channel_manager.get_channels():
            self.mqtt_client.subscribe(channel)

    def publish(self, packet):
        serializedMessage = packet.serialize()
        self.mqtt_client.publish(packet.channel, serializedMessage)
