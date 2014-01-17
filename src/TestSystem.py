#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                             T E S T   S Y S T E M                            |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet
from Importer import Importer
from DRPredictor import DRPredictor
from DRTransmitter import DRTransmitter
from ADRTransmitter import ADRTransmitter
from SynchTransmitter import SynchTransmitter
from Reconstructor import Reconstructor
import pylab 
import scipy


# Script variables
# ------------------------------------------------------------------------------------
root = "C:/Documents and Settings/Fred.FSTAKEM/My Documents/Research Thesis/" \
       "Year 2008 to 2009/Papers/AdaptiveThreshold/Data/Movements_5_1_08/"
outputRoot = "C:/Documents and Settings/Fred.FSTAKEM/My Documents/Research Thesis/" \
             "Year 2008 to 2009/Papers/AdaptiveThreshold/Temp/"
movement = "Stacking"
simulation = 1
inputFile = root + movement + "/Simulation" + str(simulation) + "/positionLog.txt"
filterLimits = [17000, 22000]
samplingInterval = 10
predictionInterval = 100
threshold = .03
txRate = 50
heartbeat = 500
minThreshold = 0.000025
maxThreshold = 0.05
maxDelay = 300
maxJitter = 80
networkParams = [20, 10, 0]

alpha = float(networkParams[0]) / maxDelay + float(networkParams[1]) / maxJitter
sigma = maxThreshold - alpha * (maxThreshold - minThreshold)
print sigma


# Functions
# ------------------------------------------------------------------------------------
def outputData(fileDesc, data):
    name = outputRoot + fileDesc + ".txt"
    print "Outputting data to: " + name
    fileHandle = open(name, 'w')
    for sample in data:
        fileHandle.write(str(sample) + "\n")
        
    fileHandle.close()
    
def calculateError(initialData, otherData):
    errorSample = []
    for initialSample in initialData:
        for otherSample in otherData:
            if initialSample.time == otherSample.time:
                distance = initialSample.distance(otherSample)
                errorSample.append(distance)
            
    return scipy.mean(errorSample)


# Tests
# ------------------------------------------------------------------------------------
# Initial data
importer = Importer()
importedData = importer.getInputData(inputFile, samplingInterval)
filteredData = []
for sample in importedData:
    if sample.time >= filterLimits[0] and \
       sample.time <= filterLimits[1]:
        filteredData.append(copy(sample))
outputData("InitialData", filteredData)

# Predicted data
predictor = DRPredictor()
predictedData = predictor.getPredictedData(filteredData, predictionInterval, samplingInterval)
outputData("PredictedData", predictedData)

# Transmitted packets
# DR
transmitter = DRTransmitter(heartbeat)
DRPackets = transmitter.getTransmittedPackets(threshold, predictedData)
outputData("DRTransmittedPackets", DRPackets)
# Synch
transmitter = SynchTransmitter()
synchPackets = transmitter.getTransmittedPackets(txRate, predictedData)
outputData("SynchTransmittedPackets", synchPackets)
# ADR
transmitter = ADRTransmitter(heartbeat)
delayEstimate = [ networkParams[0] ] * len(predictedData)
jitterEstimate = [ networkParams[1] ] * len(predictedData)
ADRPackets = transmitter.getTransmittedPackets(minThreshold, maxThreshold, maxDelay, \
                                               maxJitter, delayEstimate, jitterEstimate,\
                                               predictedData)
outputData("ADRTransmittedPackets", ADRPackets)

# Reconstructed data
reconstructor = Reconstructor()
DRData = reconstructor.getReconstructedData(DRPackets)
outputData("DRTransmittedData", DRData)
synchData = reconstructor.getReconstructedData(synchPackets)
outputData("SynchTransmittedData", synchData)
ADRData = reconstructor.getReconstructedData(ADRPackets)
outputData("ADRTransmittedData", ADRData)


# Output
# ------------------------------------------------------------------------------------
t1 = []
x1 = []
for sample in filteredData:
    t1.append(sample.time)
    x1.append(sample.position.x)
    
t2 = []
x2 = []
for sample in DRData:
    t2.append(sample.time)
    x2.append(sample.position.x)
    
t3 = []
x3 = []
for sample in synchData:
    t3.append(sample.time)
    x3.append(sample.position.x)
    
t4 = []
x4 = []
for sample in ADRData:
    t4.append(sample.time)
    x4.append(sample.position.x)

pylab.figure(1)  
pylab.plot(t1, x1, linewidth=2)
pylab.figure(2)  
pylab.plot(t2, x2, t3, x3, t4, x4, linewidth=2)
pylab.show()


