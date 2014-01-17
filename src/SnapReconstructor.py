#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                      S N A P   R E C O N S T R U C T O R                     |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample

class SnapReconstructor(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.rawSignal = []
        self.reconstructedSignal = []
        # Algorithm parameters
        self.samplingInterval = 10
            
    def getReconstructedSignal(self, rawSignal=[], samplingInterval=10):
        if isinstance( rawSignal, list ):
            self.rawSignal = rawSignal
        if isinstance( samplingInterval, int ) and samplingInterval > 0:
            self.samplingInterval = samplingInterval
        
        self.pullDataFromPackets()
        self.executeAlgorithm()
        
        return self.reconstructedSignal
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pullDataFromPackets(self):
		temp = []
		for packet in self.rawSignal:
			temp.append(packet.predictionSample)
			
		self.rawSignal = temp
		
    def executeAlgorithm(self):
        self.reconstructedSignal = []
        nextTimeToRecord = 0
        timeDiff = self.rawSignal[0].sample.time % self.samplingInterval
        if timeDiff == 0:
            self.reconstructedSignal.append( deepcopy(self.rawSignal[0].sample) )
            nextTimeToRecord = self.rawSignal[0].sample.time + \
                               self.samplingInterval
        else:
            change = self.samplingInterval - timeDiff
            newSample = Sample()
            newSample.time = self.rawSignal[0].sample.time + change
            newSample.position = deepcopy(self.rawSignal[0].sample.position)
            self.reconstructedSignal.append(newSample)
            nextTimeToRecord = newSample.time + self.samplingInterval
            
        for index, predictionSample in enumerate(self.rawSignal):
            if predictionSample.sample.time == nextTimeToRecord:
                 self.reconstructedSignal.append( deepcopy(predictionSample.sample) )
                 nextTimeToRecord = nextTimeToRecord + self.samplingInterval
            elif predictionSample.sample.time > nextTimeToRecord:
                 while predictionSample.sample.time > nextTimeToRecord:
                     deltaTime = nextTimeToRecord - self.rawSignal[index-1].sample.time
                     deltaTimeVector = Vector(deltaTime, deltaTime, deltaTime)
                     deltaPosition = self.rawSignal[index-1].velocity * deltaTimeVector
                     newPosition = self.rawSignal[index-1].sample.position + deltaPosition
                     newSample = Sample(nextTimeToRecord, newPosition)
                     self.reconstructedSignal.append( newSample )
                     nextTimeToRecord = nextTimeToRecord + self.samplingInterval
                     
                 if predictionSample.sample.time == nextTimeToRecord:    
                     self.reconstructedSignal.append( deepcopy(predictionSample.sample) )
                     nextTimeToRecord = nextTimeToRecord + self.samplingInterval
                       
    