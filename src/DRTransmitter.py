#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |            D E A D   R E C K O N I N G   T R A N S M I T T E R               |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet

class DRTransmitter(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, heartbeatRate):
        # Data
        self.inputData = []
        self.transmittedPackets = []
        # Algorithm parameters
        self.distanceThreshold = 0.01
        self.heartbeatRate = 500
        
        if isinstance( heartbeatRate, int ) and heartbeatRate > 0:
            self.heartbeatRate = heartbeatRate
            
    def getTransmittedPackets(self, distanceThreshold, data):
        if isinstance( data, list ):
            self.inputData = data
        if isinstance( distanceThreshold, float ) and distanceThreshold > 0:
            self.distanceThreshold = distanceThreshold
        
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
            estimatedPosition = self.calculateEstPosition(lastTransmittedSample, \
                                                          predictionSample.sample.time)
            distance = predictionSample.sample.position.distance(estimatedPosition)
           
            if predictionSample.sample.time >= \
               ( lastTransmittedSample.sample.time + self.heartbeatRate ):
                self.transmittedPackets.append( self.createPacket(predictionSample, sequenceNumber) )
                sequenceNumber += 1
                lastTransmittedSample = predictionSample
            elif distance >= self.distanceThreshold:
                self.transmittedPackets.append( self.createPacket(predictionSample, sequenceNumber) )
                sequenceNumber += 1
                lastTransmittedSample = predictionSample
    
    def calculateEstPosition(self, lastTransmittedSample, currentTime):
        deltaTime = currentTime - lastTransmittedSample.sample.time
        deltaTimeVector = Vector(deltaTime, deltaTime, deltaTime)
        deltaPosition = lastTransmittedSample.velocity * deltaTimeVector
        estimatedPosition = lastTransmittedSample.sample.position + deltaPosition
        return estimatedPosition
    
    def createPacket(self, predictionSample, sequenceNumber):
        packet = Packet()
        packet.predictionSample = copy( predictionSample )
        packet.sequenceNumber = sequenceNumber
        packet.timeTransmitted = predictionSample.sample.time
        return packet