#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                S Y N C H R O N O U S   T R A N S M I T T E R                 |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet

class SynchTransmitter(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.inputData = []
        self.transmittedPackets = []
        # Algorithm parameters
        self.txRate = 100
            
    def getTransmittedPackets(self, txRate, data):
        if isinstance( data, list ):
            self.inputData = data
        if isinstance( txRate, int ) and txRate > 0:
            self.txRate = txRate
        
        self.executeAlgorithm()
        
        return self.transmittedPackets
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def executeAlgorithm(self):
        self.transmittedPackets = []
        sequenceNumber = 1
        # Start algorithm before loop
        self.transmittedPackets.append( self.createPacket(self.inputData[0], sequenceNumber) )
        sequenceNumber += 1
        lastTransmittedSample = self.inputData[0]
        
        for predictionSample in self.inputData:
            if predictionSample.sample.time >= \
               ( lastTransmittedSample.sample.time + self.txRate ):
                self.transmittedPackets.append( self.createPacket(predictionSample, sequenceNumber) )
                sequenceNumber += 1
                lastTransmittedSample = predictionSample
     
    def createPacket(self, predictionSample, sequenceNumber):
        packet = Packet()
        packet.predictionSample = copy( predictionSample )
        packet.sequenceNumber = sequenceNumber
        packet.timeTransmitted = predictionSample.sample.time
        return packet