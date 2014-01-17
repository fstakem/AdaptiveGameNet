#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                         R E C O N S T R U C T O R                            |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet

class Reconstructor(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.packetData = []
        self.reconstructedData = []
        # Algorithm parameters
        self.samplingInterval = 10
            
    def getReconstructedData(self, data):
        if isinstance( data, list ):
            self.packetData = data
        
        self.executeAlgorithm()
        
        return self.reconstructedData
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def executeAlgorithm(self):
        self.reconstructedData = []
        lastRecordedTime = self.packetData[-1].predictionSample.sample.time
        for index, packet in enumerate(self.packetData):
            currentSample = packet.predictionSample
            self.reconstructedData.append( copy(currentSample.sample) )
            if currentSample.sample.time < lastRecordedTime:
                nextTime = currentSample.sample.time + self.samplingInterval
                while nextTime < self.packetData[index+1].predictionSample.sample.time:
                    deltaTime = nextTime - currentSample.sample.time
                    deltaTimeVector = Vector(deltaTime, deltaTime, deltaTime)
                    deltaPosition = currentSample.velocity * deltaTimeVector
                    newPosition = currentSample.sample.position + deltaPosition
                    newSample = Sample(nextTime, newPosition)
                    self.reconstructedData.append( newSample )
                    nextTime = nextTime + self.samplingInterval
            