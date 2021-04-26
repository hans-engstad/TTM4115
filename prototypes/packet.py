from __future__ import annotations # For return annotation
import json
import base64

class Packet():

    def __init__(self, priority: int = None, channel: str = None, senderID: str = None, encodedMessage: str = None):
        self.priority = priority
        self.channel = channel
        self.senderID = senderID
        self.encodedMessage = encodedMessage
       
    def get_decoded_message(self) -> str:
        return base64.b64decode(self.encodedMessage) 

    def serialize(self) -> str:
        return json.dumps({
            "senderID": self.senderID,
            "encodedMessage": self.encodedMessage,
            "priority": self.priority,
            "channel": self.channel
        })

    @classmethod
    def deserialize(self, json : str) -> Packet:
        packet = json.loads(json)
        return Packet(
            packet['priority'], 
            packet['channel'], 
            packet['senderID'], 
            packet['encodedMessage']
        )


