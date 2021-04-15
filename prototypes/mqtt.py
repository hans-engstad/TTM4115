# TODO: Mathias
class MQTT():

    def __init__(self, player):
        self._buffer = []
        self.player = player
        

    def subscribe(self, topic):
        pass
    def publish(self, topic, message):
        # Simluate by putting message in the buffer
        self._buffer.append(message)
    
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
                

    def recieve(self, message):
        self.player.play(message)