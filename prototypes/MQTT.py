# TODO: Mathias

import paho.mqtt.client as mqtt
import logging
from AudioPlayer import AudioPlayer
from ChannelManager import ChannelManager

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

    def __init__(self, player : AudioPlayer, channel_manager : ChannelManager):
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

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        self._logger.debug('Incoming message to topic {}'.format(msg.topic))
        self.recieve(msg.payload)

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

    def publish(self, topic, message):
        # Simluate by putting message in the buffer
        # self._buffer.append(message)
        self.mqtt_client.publish(topic, message)

    def recieve(self, message):
        self.player.play(message)

    """
    def simulate_recieve_buffer(self):
        # Simulate that entire buffer is recieved by the client, five packages at a time
        # Running one package at a time, causes interruption in audio playback

        chunk_count = 5  # Number of chunks to play at a time from the buffer
        while(len(self._buffer) > 0):
            buffer_index = chunk_count - 1
            if len(self._buffer) < buffer_index:
                buffer_index = len(self._buffer) - 1

            # Extract data-array we want to send
            data = self._buffer[0:buffer_index]

            # Join the data-array so it is one continous string of bytes
            raw_data = b''.join(data)

            # Simulate that we are recieving this raw data
            self.recieve(raw_data)

            # Remove the data we just sent from the buffer
            self._buffer = self._buffer[buffer_index + 1:]
    """
