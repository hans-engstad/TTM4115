import paho.mqtt.client as mqtt
import logging
from AudioPlayer import AudioPlayer
from ChannelManager import ChannelManager
import json
import base64

debug_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter(
    '%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# MQTT broker address
MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

# Topics for communication
MQTT_TOPIC_INPUT = 'ttm4115/team_09/answer'
MQTT_TOPIC_OUTPUT = 'ttm4115/team_09/answer'


class MQTT():

    def __init__(self, player: AudioPlayer, channel_manager: ChannelManager):
        self._buffer = []
        self.player = player
        self.channel_manager = channel_manager

        # create client
        self._logger = logging.getLogger(__name__)
        self._logger.debug(
            'Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
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

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        self._logger.debug('Incoming message to topic {}'.format(msg.topic))
        self.recieve(msg.payload)

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

    def recieve(self, message):
        decodedPacket = json.loads(message)
        decodedPayload = base64.b64decode(decodedPacket['payload'])
        print(decodedPacket['senderID'])

        # if unformattedPacket['senderID'] != "signe":
        self.player.play(decodedPayload)

