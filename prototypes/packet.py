import json
import base64

class Packet():

    def __init__(self, priority = None, channel = None, senderID = None, encodedMessage = None):
        self.priority = priority
        self.channel = channel
        self.senderID = senderID
        self.encodedMessage = encodedMessage
       
    def get_decoded_message(self):
        return base64.b64decode(self.encodedMessage) 

    def serialize(self):
        return json.dumps({
            "senderID": self.senderID,
            "encodedMessage": self.encodedMessage,
            "priority": self.priority,
            "channel": self.channel
        })

    @classmethod
    def deserialize(self, js_object):
        packet = json.loads(js_object)
        return Packet(packet['priority'], packet['channel'], packet['senderID'], packet['encodedMessage'])

   

"""
packet = {
    "priority":"1",
    "encodedMessage":"gfijrg",
    "channel":"4",
    "senderID":"34893247382"
}

newPacket = json.dumps(packet)
newPacket2 = Packet.deserialize(newPacket)
print(newPacket2.senderID)"""