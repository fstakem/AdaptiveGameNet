#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                             P A C K E T                                      |
#  |                                                                              |
#  *------------------------------------------------------------------------------*

from copy import *

class Packet(object):

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, *args):
        self.predictionSample = None
        self.sequenceNumber = 0
        self.timeTransmitted = 0
        self.timeReceived = 0
        
        if len(args) == 1:
            if isinstance( args[0], Packet ):
                self.predictionSample = copy( args[0].predictionSample )
                self.sequenceNumber = args[0].sequenceNumber   
                self.timeTransmitted = args[0].timeTransmitted
                self.timeReceived = args[0].timeReceived
        elif len(args) == 4:
            if isinstance( args[0], PredictionSample ):
                self.predictionSample = copy( args[0].predictionSample )
            if isinstance( args[1], float ) or isinstance( args[1], int ):
                self.sequenceNumber = args[1]   
            if isinstance( args[2], float ) or isinstance( args[2], int ):
                self.timeTransmitted = args[2]
            if isinstance( args[3], float ) or isinstance( args[3], int ):
                self.timeReceived = args[3]
            
    def __str__(self):
        return str( self.sequenceNumber ) + "\t" + \
               str( self.timeTransmitted )  + "\t" + \
               str( self.timeReceived ) + "\t" + \
               str( self.predictionSample )
                 
   