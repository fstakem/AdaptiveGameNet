#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                             N E T W O R K                                    |
#  |                                                                              |
#  '------------------------------------------------------------------------------'
from copy import *
from numpy.random import *
import scipy.stats 

class Network(object):

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        #Data
        self.transmittedPackets = []
        self.receivedPackets = []
        # Network parameters
        self.delay = 100
        self.jitter = 10
        self.packetLoss = 0
         
    def getReceivedPackets(self, transmittedPackets=[], delay=100, jitter=10, packetLoss=0):
        if isinstance(  transmittedPackets, list ):
            self.transmittedPackets = transmittedPackets
        if isinstance( delay, int ) and delay > 0:
             self.delay = delay
        if isinstance( jitter, int ) and jitter > 0:
            self.jitter = jitter
        if isinstance( packetLoss, int ) and  packetLoss >= 0:
            self.packetLoss = packetLoss
              
        self.simulateNetwork()
        
        return self.receivedPackets
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def simulateNetwork(self):
        self.receivedPackets = []
        
        for packet in self.transmittedPackets:
            if self.simulatePacketLoss() == False:
                delay = self.simulateDelay()
                packet.timeReceived = packet.timeTransmitted + delay
                receivedPacket = deepcopy(packet)
                self.receivedPackets.append(receivedPacket)
                
    def simulateDelay(self):
        mean = self.delay
        std = self.jitter
        while 1:
            delay = int(normal( mean, std, 1 )[0])
            if delay > 0:
                return delay
       
    def simulatePacketLoss(self):
        dropPacket = False
        if uniform( 0, 100, 1 )[0] <= self.packetLoss:
            dropPacket = True
        return dropPacket
   