import paho.mqtt.client as mqtt
import logging
from AudioPlayer import AudioPlayer
from ChannelManager import ChannelManager
import json
import base64
import logging
from AudioPlayer import AudioPlayer
from stmpy import Driver
from pyaudio import PyAudio


# MQTT broker address
MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

# Topics for communication
MQTT_TOPIC_INPUT = 'ttm4115/team_09/answer'
MQTT_TOPIC_OUTPUT = 'ttm4115/team_09/answer'


class MQTT():

    def __init__(self, driver: Driver, channel_manager: ChannelManager, py_audio: PyAudio):
        self.logger = logging.getLogger("WalkieTalkie")
        self.players = {}  # userID -> audio player object
        self.channel_manager = channel_manager
        self.driver = driver
        self.py_audio = py_audio

        # create client
        self.logger.info(
            f'Connecting to MQTT broker {MQTT_BROKER} at port {MQTT_PORT}')
        self.mqtt_client = mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # subscribe to proper topic(s) of your choice
        self.mqtt_client.subscribe(MQTT_TOPIC_INPUT)
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        self.update_subscriptions()

    def getNewPlayer(self):
        return AudioPlayer(self.driver, self.py_audio)

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self.logger.info(f'Successfully connected to MQTT broker')

    def on_message(self, client, userdata, msg):
        self.logger.debug(f'Incoming message to topic {msg.topic}')
        self.receive(msg.payload)

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

    def publish(self, topic, message):
        self.mqtt_client.publish(topic, message)

    def receive(self, message):
        decodedPacket = json.loads(message)
        decodedPayload = base64.b64decode(decodedPacket['payload'])
        senderID = decodedPacket['senderID']

        if senderID != self.channel_manager.getUserID():
            if senderID not in self.players:
                newPlayer = self.getNewPlayer()
                self.players[senderID] = newPlayer

            self.players[senderID].play(decodedPayload)
