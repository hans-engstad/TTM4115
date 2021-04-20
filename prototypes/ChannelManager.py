import uuid
import logging


class ChannelManager():
    def __init__(self):
        self.logger = logging.getLogger("WalkieTalkie")
        self._channels = ["ttm4115/team_09/answer"]
        self.userID = uuid.uuid1().hex

    def get_channels(self):
        return self._channels

    def add_channel(self, channel):
        self.logger.info(f'Subscribed to {channel}')
        self._channels.append(channel)

    def getUserID(self):
        return self.userID
