#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                F I N D   M I N I M U M   T H R E S H O L D                   |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Globals import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet
from PredictionSample import PredictionSample
from Importer import Importer
from DRPredictor import DRPredictor
from DRTransmitter import DRTransmitter
from Reconstructor import Reconstructor
from PartAResult import PartAResult
import pylab 
import scipy


# Script variables
# ------------------------------------------------------------------------------------
root = "C:/Documents and Settings/Fred.FSTAKEM/My Documents/Research Thesis/" \
       "Year 2008 to 2009/Papers/AdaptiveThreshold/Data/Movements_5_1_08/"
outputRoot = "C:/Documents and Settings/Fred.FSTAKEM/My Documents/Research Thesis/" \
             "Year 2008 to 2009/Papers/AdaptiveThreshold/Temp/"
movements = [ "Stacking" , "CatchBlock", "TieShoes" ]
simulations = [ [1, 3], [1, 3], [1, 3] ]
files = []
samplingInterval = 10
predictionInterval = 100
minThreshold = 0.000025
maxThreshold = 0.05
thresholds = scipy.linspace( minThreshold, maxThreshold, 20 )
heartbeat = 500


# Functions
# ------------------------------------------------------------------------------------
def createInputFiles():
    root = "C:/Documents and Settings/Fred.FSTAKEM/My Documents/Research Thesis/" \
           "Year 2008 to 2009/Papers/AdaptiveThreshold/Data/Movements_5_1_08/"
    for index, movement in enumerate(movements):
        simulationStart = simulations[index][0]
        simulationEnd = simulations[index][1]
        for simulation in range(simulationStart, simulationEnd + 1):
            inputFile = root + movement + "/Simulation" + str(simulation) + "/positionLog.txt"
            files.append(inputFile)
            
def findMovementType(fileName):
    movement = fileName.split('/')[-3]
    if movement == "Stacking":
        movement = MovementType.Stacking
    elif movement == "CatchBlock":
        movement = MovementType.Catching
    elif movement == "TieShoes":
        movement = MovementType.TieShoes
       
    return movement
            
def calculateTransmissionRate(initialData, transmittedPackets):
    timeOfSignal = initialData[-1].time - initialData[0].time
    numOfPacketsSent = len(transmittedPackets)
    msPerPacket = float(timeOfSignal) / float(numOfPacketsSent)
    return msPerPacket

def calculateError(initialData, otherData):
    errorSample = []
    for initialSample in initialData:
        for otherSample in otherData:
            if initialSample.time == otherSample.time:
                distance = initialSample.distance(otherSample)
                errorSample.append(distance)
                
    return scipy.mean(errorSample)
            
def runSimulation():
    totalResults = []    
    for file in files:
        print "Working on: " + file.split('/')[-2]
        # Initial data ---------------------------------------------------------------
        importer = Importer()
        importedData = importer.getInputData(file, samplingInterval)
        
        #PredictedData ---------------------------------------------------------------
        predictor = DRPredictor()
        predictedData = predictor.getPredictedData(importedData, predictionInterval, \
                                                   samplingInterval)
            
        for threshold in thresholds:
            #Transmitted packets and data ---------------------------------------------
            transmitter = DRTransmitter(heartbeat)
            transmittedPackets = transmitter.getTransmittedPackets(threshold, predictedData)
            reconstructor = Reconstructor()
            transmittedData = reconstructor.getReconstructedData(transmittedPackets)
            
            result = PartAResult()
            result.movementType = findMovementType(file)
            result.threshold = threshold
            result.txRate = calculateTransmissionRate(importedData, transmittedPackets)
            result.txError = calculateError(importedData, transmittedData)
            totalResults.append(result)
            
    return totalResults
                       
def seperateResults(totalResults):
    stackingResults = []
    catchingResults = []
    tieShoesResults = []
    for result in totalResults:
        if result.movementType == MovementType.Stacking:
            stackingResults.append( copy(result) )
        elif result.movementType == MovementType.Catching:
            catchingResults.append( copy(result) )
        elif result.movementType == MovementType.TieShoes:
            tieShoesResults.append( copy(result) )
            
    return [ stackingResults, catchingResults, tieShoesResults ]
            
def condenseResults(results):
    newResults = []
    for threshold in thresholds:
        tempTxError = []
        tempTxRate = []
        for result in results:
            if result.threshold == threshold:
                tempTxError.append( result.txError )
                tempTxRate.append( result.txRate )
                
        newResult = PartAResult()
        newResult.movementType = results[0].movementType
        newResult.threshold = threshold
        newResult.txError = scipy.mean( tempTxError )
        newResult.txRate = scipy.mean( tempTxRate )
        newResults.append( newResult )
    
    return newResults


# Test script
# ------------------------------------------------------------------------------------
createInputFiles()
totalResults = runSimulation()
seperateResults = seperateResults(totalResults)

for results in seperateResults:
    finalResults = condenseResults(results)
    
    for result in finalResults:
        print result
        
    print