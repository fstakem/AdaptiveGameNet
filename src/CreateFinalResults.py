#!/usr/bin/env python
# encoding: utf-8
"""
CreateFinalResults.py

Created by Fredrick Stakem on 2010-02-16.
Copyright (c) 2010 __Georgia Tech__. All rights reserved.
"""

# Libraries
# ------------------------------------------------------------------------------------
import sys
import os
from copy import *
import pylab 
import scipy

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
from Network import Network
from Receiver import Receiver
from SnapReconstructor import SnapReconstructor


# Folders and external libraries
# ------------------------------------------------------------------------------------
currentDir = os.path.abspath(sys.path[0])
parentDir = os.path.dirname(sys.path[0])
pyEnumRelative = os.path.join('PyEnum', 'enum-0.4.3-py2.5.egg')
pyEnumPath = os.path.join(parentDir, pyEnumRelative)
sys.path.append(pyEnumPath)
from enum import Enum
sys.path.pop()

# Script variables
# ------------------------------------------------------------------------------------
root = "/Users/fstakem/Research/AdaptiveThreshold/"
outputRoot = root + "Temp/"
data = "/Users/fstakem/Data/Movements_5_1_08/"
movement = "Stacking"
simulation = 1
inputFile = data + movement + "/Simulation" + str(simulation) + "/positionLog.txt"
filterLimits = [17000, 22000]
samplingInterval = 10
predictionInterval = 100
threshold = .03
heartbeat = 500
minThreshold = 0.00025
maxThreshold = 0.05
maxDelay = 300
maxJitter = 80
networkParams = [140, 20, 0]

# Functions
# ------------------------------------------------------------------------------------
def outputData(fileDesc, data):
    name = outputRoot + fileDesc + ".txt"
    print "Outputting data to: " + name
    fileHandle = open(name, 'w')
    for sample in data:
        fileHandle.write(str(sample) + "\n")
        
    fileHandle.close()

# Simulate the system
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
DRTxPackets = transmitter.getTransmittedPackets(threshold, predictedData)
outputData("DRTransmittedPackets", DRTxPackets)
# ADR
transmitter = ADRTransmitter(heartbeat)
delayEstimate = [ networkParams[0] ] * len(predictedData)
jitterEstimate = [ networkParams[1] ] * len(predictedData)
ADRTxPackets = transmitter.getTransmittedPackets(minThreshold, maxThreshold, maxDelay, \
                                                 maxJitter, delayEstimate, jitterEstimate,\
                                                 predictedData)
outputData("ADRTransmittedPackets", ADRTxPackets)

# Reconstructed transmitted data
reconstructor = SnapReconstructor()
DRTxData = reconstructor.getReconstructedSignal(DRTxPackets, samplingInterval)
outputData("DRTransmittedData", DRTxData)
ADRTxData = reconstructor.getReconstructedSignal(ADRTxPackets, samplingInterval)
outputData("ADRTransmittedData", ADRTxData)

# Simulate network
network = Network()
DRRxPackets = network.getReceivedPackets(DRTxPackets, networkParams[0], networkParams[1], \
									     networkParams[2])
outputData("DRReceivedPackets", DRRxPackets)
ADRRxPackets = network.getReceivedPackets(ADRTxPackets, networkParams[0], networkParams[1], \
									      networkParams[2])
outputData("ADRReceivedPackets", ADRRxPackets)

# Received data
receiver = Receiver()
DRRxData = receiver.getFilteredData(DRRxPackets)
outputData("DRReceivedData", DRRxData)
ADRRxData = receiver.getFilteredData(ADRRxPackets)
outputData("ADRReceivedData", ADRRxData)

# Reconstructed received data
DRRxReconData = reconstructor.getReconstructedSignal(DRRxData, samplingInterval)
outputData("DRRxReconData", DRRxReconData)
ADRRxReconData = reconstructor.getReconstructedSignal(ADRRxData, samplingInterval)
outputData("ADRRxReconData", ADRRxReconData)

# Output
# ------------------------------------------------------------------------------------
t1 = []
x1 = []
for sample in filteredData:
    t1.append(sample.time)
    x1.append(sample.position.x)
    
t2 = []
x2 = []
for sample in DRTxData:
    t2.append(sample.time)
    x2.append(sample.position.x)
    
t3 = []
x3 = []
for sample in ADRTxData:
    t3.append(sample.time)
    x3.append(sample.position.x)

t4 = []
x4 = []
for sample in DRRxReconData:
    t4.append(sample.time)
    x4.append(sample.position.x)

t5 = []
x5 = []
for sample in ADRRxReconData:
    t5.append(sample.time)
    x5.append(sample.position.x)

pylab.figure(1)  
pylab.plot(t1, x1, linewidth=2)
pylab.figure(2)  
pylab.plot(t2, x2, 'k', t3, x3, 'b', linewidth=2)
pylab.figure(3)  
pylab.plot(t4, x4, 'k', t5, x5, 'b', linewidth=2)
pylab.show()