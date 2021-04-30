import uuid
import logging


class ServerAPI():
    def __init__(self):
        self.logger = logging.getLogger("WalkieTalkie")
        self.channels = self._get_preconfigured_channels()
        self.userID = self._authenticate()

    def _authenticate(self) -> None:
        """Emulated authentication request to OAuth API"""
        authenticated = True # server authenticates the user
        if authenticated:
            return uuid.uuid1().hex
        return None

    def _get_preconfigured_channels(self) -> list:
        """Emulated response from server of channels
        everyone will have been pre-subscribed to"""
        
        authorized = True # server checks credentials 
        if authorized:
            response = [
                "ttm4115/team_09/emergency"
            ]
        else:
            response = []
        return response

    def getAvailableChannels(self) -> list:
        """Emulated response from server of channels
        thats possible for everyone to join"""
        authorized = True # server checks credentials
        if authorized:
            response = [
                "ttm4115/team_09/channel1",
                "ttm4115/team_09/channel2"
            ]
        else:
            response = []
        return response

    def getChannelPriority(self,channel : str) -> int:
        """Emulated response from server mapping channels
        to a priority level"""

        response = {
            "ttm4115/team_09/channel1":1,
            "ttm4115/team_09/emergency":3
        }

        if channel in response:
            return response[channel]

        # default priority level
        return 1

    def get_channels(self) -> list:
        return self.channels


    def add_channel(self, channel : str) -> bool:
        authorized = True  # server checks credentials 
        if authorized:
            if channel not in self.channels:
                self.logger.info(f'Subscribed to {channel}')
                self.channels.append(channel)
                return True
            
            self.logger.info(f'Already subscribed to {channel}')
            return False
        else:
            return False

    def getUserID(self) -> str:
        return self.userID


    


   
