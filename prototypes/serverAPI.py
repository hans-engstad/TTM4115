import uuid
import logging


class ServerAPI():
    def __init__(self):
        self.logger = logging.getLogger("WalkieTalkie")
        self._channels = self._get_preconfigured_channels()
        self.userID = None
        self._authenticate()

    def _authenticate(self) -> None:
        # fake API call

        authenticated = True
        if authenticated:
            self.userID = uuid.uuid1().hex


    def _get_preconfigured_channels(self) -> list:
        # fake API call
        return  [
            "ttm4115/team_09/channel1",
            "ttm4115/team_09/emergency"
        ]

    def get_channels(self) -> list:
        return self._channels

    def add_channel(self, channel : str) -> None:
        self.logger.info(f'Subscribed to {channel}')
        self._channels.append(channel)

    def getUserID(self) -> str:
        return self.userID

    def getAvailableChannels(self) -> list:
        # fake API call
        return [ 
            "ttm4115/team_09/channel1",
            "ttm4115/team_09/channel2",
            "ttm4115/team_09/emergency"
        ]


    def getChannelPriority(self,channel : str) -> int:
        # fake API call
        priorities = {
            "ttm4115/team_09/channel1":1,
            "ttm4115/team_09/emergency":3
        }

        if channel in priorities:
            return priorities[channel]
    
        return 1

   
