#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |               D E A D   R E C K O N I N G   P R E D I C T O R                |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
import scipy
import scipy.interpolate as interpolate
from Vector import Vector
from PredictionSample import PredictionSample

class DRPredictor():
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.inputData = []
        self.predictedData = []
        # Data parameters
        self.predictionInterval = 100
        self.samplingInterval = 10
    
    def getPredictedData(self, data, predictionInterval=100, samplingInterval=10):
        self.inputData = data
        self.predictionInterval = predictionInterval
        self.samplingInterval = samplingInterval
        
        self.executeAlgorithm()
        
        return self.predictedData
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def executeAlgorithm(self):
        self.predictedData = []
        
        for index, sample in enumerate(self.inputData):
            if sample.time < self.predictionInterval:
                # Set initial values
                predictionSample = PredictionSample()
                predictionSample.sample = copy(sample)
                predictionSample.velocity = Vector()
                self.predictedData.append( predictionSample )
            else:
                shift = index - self.predictionInterval / self.samplingInterval
                
                # Calculate velocity
                deltaPosition = self.inputData[index].position - \
                                self.inputData[shift].position
                deltaTime = self.inputData[index].time - \
                            self.inputData[shift].time
                invDeltaTimeVector = Vector( 1 / float(deltaTime), \
                                             1 / float(deltaTime), \
                                             1 / float(deltaTime))
                velocity = deltaPosition * invDeltaTimeVector
                               
                # Populate data structures  
                predictionSample = PredictionSample()            
                predictionSample.sample = copy(sample)
                predictionSample.velocity = velocity
                self.predictedData.append( predictionSample )
                