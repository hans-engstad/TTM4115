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
        # while(len(self._buffer) > 0):
        #     data = self._buffer.pop(0)
        self.recieve(b''.join(self._buffer))
        self._buffer = []

    def recieve(self, message):
        self.player.state_machine.send("play", args=[message])