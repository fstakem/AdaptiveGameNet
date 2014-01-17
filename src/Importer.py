#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                           I M P O R T E R                                    |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

import scipy
import scipy.interpolate as interpolate
from copy import *
from Vector import Vector
from Sample import Sample

class Importer(object):

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.rawData = []
        
        # Constants
        self.samplingInterval = 10
        self.scalingFactorA = Vector( 2.40, 4.40, -2.60 )
        self.scalingFactorB = Vector( (1/2.10), (1/3.10), (1/0.65) )
        self.minutePosition = 1
        self.secondPosition = 2
        self.millisecondPosition = 3
        self.xPosition = 9
        self.yPosition = 10
        self.zPosition = 11
        self.numberOfPaddingSamples = 200
    
    def getInputData(self, fileName, samplingInterval):
        self.samplingInterval = samplingInterval
        self.rawData = []
        
        self.importData(fileName)
        self.removeDuplicateSamples()
        self.resampleData()
        self.shiftData()
        self.padData()
        self.scaleData()
    
        return self.rawData
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def importData(self, fileName):
        input = open( fileName, 'r' )
        for line in input:
            tokens = line.split('\t')
            sample = Sample()
            
            minutes = int( tokens[self.minutePosition] )
            seconds = int( tokens[self.secondPosition] )
            milliseconds = int( tokens[self.millisecondPosition] )
            sample.time = minutes * 60 * 1000 + seconds * 1000 + milliseconds
            sample.position.x = float( tokens[self.xPosition] )
            sample.position.y = float( tokens[self.yPosition] )
            sample.position.z = float( tokens[self.zPosition] )
            self.rawData.append(sample)
			
        input.close()
    
    def removeDuplicateSamples(self):
        tempData = []
        tempData.append(self.rawData[0])
        
        for sample in self.rawData:
            lastTimeSaved = tempData[-1].time
            if sample.time > lastTimeSaved:
                tempData.append(sample)
        
        self.rawData = tempData
    
    def resampleData(self):
        tempData = []
        tempData.append(self.rawData[0])
        lastRecordedTime = tempData[-1].time
        nextTimeToRecord = lastRecordedTime + self.samplingInterval
        
        for index, sample in enumerate(self.rawData):
            if sample.time == nextTimeToRecord:
                tempData.append(sample)
                lastRecordedTime = nextTimeToRecord
                nextTimeToRecord = lastRecordedTime + self.samplingInterval
            elif sample.time > nextTimeToRecord:
                interpolationSamples = [ self.rawData[index-1], sample ]
                while sample.time >= nextTimeToRecord:
                    interpolatedSample = self.interpolate(interpolationSamples, \
                                                          nextTimeToRecord) 
                    tempData.append( interpolatedSample )
                    lastRecordedTime = nextTimeToRecord
                    nextTimeToRecord = lastRecordedTime + self.samplingInterval
        
        self.rawData = tempData
        
    def interpolate(self, samples, currentTime):
        newSample = Sample()
        newSample.time = currentTime
        
        time = [ samples[0].time, samples[1].time ]
        x = [ samples[0].position.x, samples[1].position.x ]
        y = [ samples[0].position.y, samples[1].position.y ]
        z = [ samples[0].position.z, samples[1].position.z ]
        
        interpolationFunction = interpolate.interp1d( time, x )
        newSample.position.x = interpolationFunction(currentTime).flatten()[0]
        interpolationFunction = interpolate.interp1d( time, y )
        newSample.position.y = interpolationFunction(currentTime).flatten()[0]
        interpolationFunction = interpolate.interp1d( time, z )
        newSample.position.z = interpolationFunction(currentTime).flatten()[0]
        
        return newSample
    
    def shiftData(self):
        tempData = []
        firstTime = self.rawData[0].time
        
        for sample in self.rawData:
            if sample.time >= firstTime:
                newSample = Sample()
                newSample.time = sample.time - firstTime + ( 10 * self.numberOfPaddingSamples) 
                newSample.position = copy( sample.position )
                tempData.append(newSample)
        
        self.rawData = tempData
        
    def padData(self):
        tempData = []
        
        for index in range(0, self.numberOfPaddingSamples):
            newSample = copy( self.rawData[0] )
            newSample.time = index * 10
            tempData.append(newSample)
            
        for sample in self.rawData:
            tempData.append(sample)
            
        for index in range(0, self.numberOfPaddingSamples):
            newSample = copy( self.rawData[-1] )
            newSample.time = newSample.time + ( ( index + 1) * 10 )
            tempData.append(newSample)
            
        self.rawData = tempData
        
    def scaleData(self):
        tempData = []
        
        for sample in self.rawData:
            newSample = Sample()
            newSample.time = sample.time
            newSample.position = ( sample.position + self.scalingFactorA ) 
            newSample.position.x = newSample.position.x * self.scalingFactorB.x
            newSample.position.y = newSample.position.y * self.scalingFactorB.y
            newSample.position.z = newSample.position.z * self.scalingFactorB.z
            newSample.position = newSample.position - Vector(1,1,1)
            tempData.append(newSample)
        
        self.rawData = tempData        

