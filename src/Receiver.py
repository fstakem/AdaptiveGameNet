#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                             R E C E I V E R                                  |
#  |                                                                              |
#  '------------------------------------------------------------------------------'
from copy import *
import operator

class Receiver(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.receivedPackets = []
        self.filteredPackets = []
        
    def getFilteredData(self, receivedPackets=[]):
        if isinstance( receivedPackets, list ):
            self.receivedPackets = receivedPackets
        
        self.filterPackets()
        self.setTime()
        
        return self.filteredPackets
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def filterPackets(self):
        # Remove packets received at same time and out of order packets
        self.filteredPackets = []
        self.receivedPackets.sort( key = operator.attrgetter('timeReceived') )
        self.filteredPackets.append(deepcopy(self.receivedPackets[0]))
        lastPacketReceived = self.receivedPackets[0]
        for packet in self.receivedPackets:
            if packet.timeReceived == lastPacketReceived.timeReceived:
               if packet.sequenceNumber > lastPacketReceived.sequenceNumber:
                   self.filteredPackets[-1] = deepcopy(packet)
                   lastPacketReceived = packet
            else:
                if packet.sequenceNumber > lastPacketReceived.sequenceNumber:
                    self.filteredPackets.append(deepcopy(packet))
                    lastPacketReceived = packet

    def setTime(self):
		for packet in self.filteredPackets:
			packet.predictionSample.sample.time = packet.timeReceived
    
    