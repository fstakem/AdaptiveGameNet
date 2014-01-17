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
simulation = range(1,41)
inputFiles = []
for i in simulation:
	inputFile = data + movement + "/Simulation" + str(i) + "/positionLog.txt"
	inputFiles.append(inputFile)
filterLimits = [17000, 22000]
samplingInterval = 10
predictionInterval = 100
threshold = .03
heartbeat = 500
minThreshold = 0.00025
maxThreshold = 0.05
maxDelay = 300
maxJitter = 80
networkParams = []

delay = None
jitter = None
packetLoss = 0

# Delay
delay = range(10,260,5)
jitter = 30
for d in delay:
	networkParams.append([d, jitter, packetLoss])
	
# Jitter
#delay = 100
#jitter = range(5, 65, 5)
#for j in jitter:
#	networkParams.append([delay, j, packetLoss])

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

# Simulate the system
# ------------------------------------------------------------------------------------
overallError = []

for params in networkParams:
	errorDRTx = []
	errorADRTx = []
	errorDRRx = []
	errorADRRx = []
	
	for i, fileName in enumerate(inputFiles):
		# Status
		print "Working on delay: %d  simulation: %d" % (params[0], i+1)
		#print "Working on jitter: %d  simulation: %d" % (params[1], i+1)
		
		# Initial data
		importer = Importer()
		importedData = importer.getInputData(fileName, samplingInterval)
		filteredData = []
		for sample in importedData:
		    if sample.time >= filterLimits[0] and \
		       sample.time <= filterLimits[1]:
		        filteredData.append(copy(sample))

		# Predicted data
		predictor = DRPredictor()
		predictedData = predictor.getPredictedData(filteredData, predictionInterval, samplingInterval)
	
		# Transmitted packets
		# DR
		transmitter = DRTransmitter(heartbeat)
		DRTxPackets = transmitter.getTransmittedPackets(threshold, predictedData)
		# ADR
		transmitter = ADRTransmitter(heartbeat)
		delayEstimate = [ params[0] ] * len(predictedData)
		jitterEstimate = [ params[1] ] * len(predictedData)
		ADRTxPackets = transmitter.getTransmittedPackets(minThreshold, maxThreshold, maxDelay, \
		                                                 maxJitter, delayEstimate, jitterEstimate,\
		                                                 predictedData)

		# Reconstructed transmitted data
		reconstructor = SnapReconstructor()
		DRTxData = reconstructor.getReconstructedSignal(DRTxPackets, samplingInterval)
		ADRTxData = reconstructor.getReconstructedSignal(ADRTxPackets, samplingInterval)

		# Simulate network
		network = Network()
		DRRxPackets = network.getReceivedPackets(DRTxPackets, params[0], params[1], \
											     params[2])
		ADRRxPackets = network.getReceivedPackets(ADRTxPackets, params[0], params[1], \
											      params[2])

		# Received data
		receiver = Receiver()
		DRRxData = receiver.getFilteredData(DRRxPackets)
		ADRRxData = receiver.getFilteredData(ADRRxPackets)

		# Reconstructed received data
		DRRxReconData = reconstructor.getReconstructedSignal(DRRxData, samplingInterval)
		ADRRxReconData = reconstructor.getReconstructedSignal(ADRRxData, samplingInterval)
	
		# Calculate results
		errorDRTx.append(calculateError(filteredData, DRTxData))
		errorADRTx.append(calculateError(filteredData, ADRTxData)) 
		errorDRRx.append(calculateError(filteredData, DRRxReconData)) 
		errorADRRx.append(calculateError(filteredData, ADRRxReconData)) 
		
	overallError.append([params[0], scipy.mean(errorDRTx), scipy.mean(errorADRTx), 
						scipy.mean(errorDRRx), scipy.mean(errorADRRx)])
	#overallError.append([params[1], scipy.mean(errorDRTx), scipy.mean(errorADRTx), 
	#					scipy.mean(errorDRRx), scipy.mean(errorADRRx)])

# Output
# ------------------------------------------------------------------------------------
x = []
y1 = []
y2 = []
y3 = []
y4 = []

for error in overallError:
	x.append(error[0])
	y1.append(error[1])
	y2.append(error[2])
	y3.append(error[3])
	y4.append(error[4])
	print str(error[0]) + "\t" + str(error[1]) + "\t" + str(error[2]) + "\t" + str(error[3]) + "\t" + str(error[4])

pylab.figure(1)  
pylab.plot(x, y1, 'k', x, y2, 'b', x, y3, 'k--', x, y4, 'b--', linewidth=2)
pylab.show()

