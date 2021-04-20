class ChannelManager():
    def __init__(self):
        self._channels = ["Kanal 1", "Kanal 2"]
    
    def get_channels(self):
        return self._channels
    
    def add_channel(self, channel):
        self._channels.append(channel)