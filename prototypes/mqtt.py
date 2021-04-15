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
        # Simulate that entire buffer is recieved by client, one package at a time
        chunk_count = 10  # Number of chunks to play at a time from the buffer
        while(len(self._buffer) > 0):
            data = []
            buffer_index = 9
            if len(self._buffer) < buffer_index:
                buffer_index = len(self._buffer) - 1
            
            print("Buffer length: ", len(self._buffer))
            print("Buffer index: ", buffer_index)

            data = self._buffer[0:buffer_index]
            raw_data = b''.join(data)
            
            self.recieve(raw_data)
            self._buffer = self._buffer[buffer_index+1:]
        # self.recieve(b''.join(self._buffer))
        self._buffer = []

    def recieve(self, message):
        self.player.state_machine.send("play", args=[message])