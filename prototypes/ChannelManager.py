import uuid


class ChannelManager():
    def __init__(self):
        self._channels = ["ttm4115/team_09/answer"]
        self.userID = uuid.uuid1().hex

    def get_channels(self):
        return self._channels

    def add_channel(self, channel):
        self._channels.append(channel)

    def getUserID(self):
        return self.userID
