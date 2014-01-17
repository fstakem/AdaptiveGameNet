#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |               A D A P T I V E   D R   T R A N S M I T T E R                  |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet

class ADRTransmitter(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, heartbeatRate):
        # Data
        self.inputData = []
        self.transmittedPackets = []
        self.delayEstimate = []
        self.jitterEstimate = []
        # Algorithm parameters
        self.heartbeatRate = 500
        self.minThreshold = 0.01
        self.maxThreshold = 0.1
        self.maxDelay = 200
        self.maxJitter = 50
        
        if isinstance( heartbeatRate, int ) and heartbeatRate > 0:
            self.heartbeatRate = heartbeatRate
        
    def getTransmittedPackets(self, minThreshold, maxThreshold, maxDelay, \
                              maxJitter, delayEstimate, jitterEstimate, data):
        if isinstance( data, list ):
            self.inputData = data
        if isinstance( minThreshold, float ) and minThreshold > 0:    
            self.minThreshold = minThreshold
        if isinstance( maxThreshold, float ) and maxThreshold > 0:
            self.maxThreshold = maxThreshold
        if isinstance( maxDelay, int ) and maxDelay > 0:
            self.maxDelay = maxDelay
        if isinstance( maxJitter, int ) and maxJitter > 0:
            self.maxJitter = maxJitter
      
        if isinstance( delayEstimate, list ):
            self.delayEstimate = delayEstimate
        if isinstance( jitterEstimate, list ):
            self.jitterEstimate = jitterEstimate
        
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
        
        for index, predictionSample in enumerate(self.inputData):
            estimatedPosition = self.calculateEstPosition(lastTransmittedSample, \
                                                          predictionSample.sample.time)
            distance = predictionSample.sample.position.distance(estimatedPosition)
            delay = self.delayEstimate[index]
            jitter = self.jitterEstimate[index]
            threshold = self.calculateThreshold(delay, jitter)
           
            if predictionSample.sample.time >= \
               ( lastTransmittedSample.sample.time + self.heartbeatRate ):
                self.transmittedPackets.append( self.createPacket(predictionSample, sequenceNumber) )
                sequenceNumber += 1
                lastTransmittedSample = predictionSample
            elif distance >= threshold:
                self.transmittedPackets.append( self.createPacket(predictionSample, sequenceNumber) )
                sequenceNumber += 1
                lastTransmittedSample = predictionSample
                  
    def calculateThreshold(self, delay, jitter):
        thresholdDifference = self.maxThreshold - self.minThreshold
        delayFactor = float(delay) / self.maxDelay
        jitterFactor = float(jitter) / self.maxJitter
        alpha = delayFactor + jitterFactor
        if alpha > 1:
            alpha = 1
        threshold = self.maxThreshold - alpha * thresholdDifference
        
        return threshold
    
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