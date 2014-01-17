#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                    C O M P A R E   A L G O R I T H M S                       |
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
from ADRTransmitter import ADRTransmitter
from SynchTransmitter import SynchTransmitter
from Reconstructor import Reconstructor
from PartAResult import PartAResult
from PartBResult import PartBResult
import pylab 
import scipy


# Script variables
# ------------------------------------------------------------------------------------
testType = TestType.DelayJitter
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
thresholds = scipy.linspace( minThreshold, maxThreshold, 40 )
minTxRate = 10
maxTxRate = 500
txRates = scipy.linspace( minTxRate, maxTxRate, 40 )
delays = []
jitters = []
maxDelay = 300
maxJitter = 80
heartbeat = 500

if testType == TestType.Delay:
    delays = range(10,405,5)
    jitters = [ 20 ] * len(delays)
elif testType == TestType.Jitter:
    jitters = range(2,102,2)
    delays = [ 100 ] * len(jitters)
else:
    d = range(10,260,10)
    j = [5] * len(d)
    delays.extend(d)
    jitters.extend(j)
    
    d = range(10,260,10)
    j = [10] * len(d)
    delays.extend(d)
    jitters.extend(j)
    
    d = range(10,260,10)
    j = [20] * len(d)
    delays.extend(d)
    jitters.extend(j)
    
    d = range(10,260,10)
    j = [30] * len(d)
    delays.extend(d)
    jitters.extend(j)
    
    d = range(10,260,10)
    j = [40] * len(d)
    delays.extend(d)
    jitters.extend(j)
    
    d = range(10,260,10)
    j = [50] * len(d)
    delays.extend(d)
    jitters.extend(j)
    
    d = range(10,260,10)
    j = [60] * len(d)
    delays.extend(d)
    jitters.extend(j)
    

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

def simulateDR():
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
            
            result = PartBResult()
            result.movementType = findMovementType(file)
            result.threshold = threshold
            result.txRate = calculateTransmissionRate(importedData, transmittedPackets)
            result.txError = calculateError(importedData, transmittedData)
            totalResults.append(result)
                
    return totalResults

def simulateSynch():
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
        
        for txRate in txRates:
            #Transmitted packets and data ---------------------------------------------
            transmitter = SynchTransmitter()
            transmittedPackets = transmitter.getTransmittedPackets(int(txRate), predictedData)
            reconstructor = Reconstructor()
            transmittedData = reconstructor.getReconstructedData(transmittedPackets)
            
            result = PartBResult()
            result.movementType = findMovementType(file)
            result.threshold = 0
            result.txRate = txRate
            result.txError = calculateError(importedData, transmittedData)
            totalResults.append(result)
            
    return totalResults

def simulateADR():
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
        
        for index, delay in enumerate(delays):
            delayList = [delay] * len(predictedData)
            jitter = jitters[index]
            jitterList = [jitter] * len(predictedData)
            transmitter = ADRTransmitter(heartbeat)
            transmittedPackets = transmitter.getTransmittedPackets(minThreshold, maxThreshold, 
                                                                   maxDelay, maxJitter, \
                                                                   delayList, jitterList, \
                                                                   predictedData)
            reconstructor = Reconstructor()
            transmittedData = reconstructor.getReconstructedData(transmittedPackets)
        
            result = PartBResult()
            result.movementType = findMovementType(file)
            result.threshold = 0
            result.txRate = calculateTransmissionRate(importedData, transmittedPackets)
            result.txError = calculateError(importedData, transmittedData)
            result.delay = delay
            result.jitter = jitter
            result.packetLoss = 0
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

def condenseByTxRate(results):
    newResults = []
    newTxRates = []
    for result in results:
        insert = True
        for txRate in newTxRates:
            if txRate == result.txRate:
                insert = False
                break
            
        if insert == True:
            newTxRates.append(result.txRate)
            
    newTxRates.sort()
    
    for txRate in newTxRates:
        tempTxError = []
        for result in results:
            if result.txRate == txRate:
                tempTxError.append(result.txError)
    
        newResult = PartAResult()
        newResult.movementType = results[0].movementType
        newResult.threshold = 0
        newResult.txError = scipy.mean( tempTxError )
        newResult.txRate = txRate
        newResults.append( newResult )
    
    return newResults

def condenseByDelay(results):
    newResults = []
    for delay in delays:
        tempTxRate = []
        tempTxError = []
        for result in results:
            if result.delay == delay:
                tempTxRate.append( result.txRate )
                tempTxError.append( result.txError )
        
        newResult = PartBResult()
        newResult.movementType = results[0].movementType
        newResult.threshold = 0
        newResult.txError = scipy.mean( tempTxError )
        newResult.txRate = scipy.mean( tempTxRate )
        newResult.delay = delay
        newResults.append( newResult )
        
    return newResults

def condenseByJitter(results):
    newResults = []
    for jitter in jitters:
        tempTxRate = []
        tempTxError = []
        for result in results:
            if result.jitter == jitter:
                tempTxRate.append( result.txRate )
                tempTxError.append( result.txError )
        
        newResult = PartBResult()
        newResult.movementType = results[0].movementType
        newResult.threshold = 0
        newResult.txError = scipy.mean( tempTxError )
        newResult.txRate = scipy.mean( tempTxRate )
        newResult.jitter = jitter
        newResults.append( newResult )
        
    return newResults


# Test script
# ------------------------------------------------------------------------------------
createInputFiles()

if testType == TestType.Delay:
    DRResults = simulateDR()
    ADRResults = simulateADR()
    
    sepDRResults = seperateResults(DRResults)
    sepADRResults = seperateResults(ADRResults)
           
    print "DR"      
    for DRResults in sepDRResults:
        results = condenseByTxRate(DRResults)
        for result in results:
            print result
     
    print "ADR"            
    for ADRResults in sepADRResults:
        results = condenseByDelay(ADRResults)
        for result in results:
            print result
            
elif testType == TestType.Jitter:
    DRResults = simulateDR()
    ADRResults = simulateADR()
    
    sepDRResults = seperateResults(DRResults)
    sepADRResults = seperateResults(ADRResults)
    
    print "DR"      
    for DRResults in sepDRResults:
        results = condenseByTxRate(DRResults)
        for result in results:
            print result
     
    print "ADR"            
    for ADRResults in sepADRResults:
        results = condenseByJitter(ADRResults)
        for result in results:
            print result
else:
    #SynchResults = simulateSynch()
    #DRResults = simulateDR()
    ADRResults = simulateADR()
    
    #sepSynchResults = seperateResults(SynchResults)
    #sepDRResults = seperateResults(DRResults)
    sepADRResults = seperateResults(ADRResults)
    
#===============================================================================
#    print "Synch"
#    for SynchResults in sepSynchResults:
#        results = condenseByTxRate(SynchResults)
#        for result in results:
#            print result
#            
#    print "DR"      
#    for DRResults in sepDRResults:
#        results = condenseByTxRate(DRResults)
#        for result in results:
#            print result
#===============================================================================
     
    print "ADR"            
    for ADRResults in sepADRResults:
        results = condenseByTxRate(ADRResults)
        for result in results:
            print result
            
