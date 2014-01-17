#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                       P A R T   A    R E S U L T S                           |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from Globals import *

class PartBResult(object):

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        self.movementType = None
        self.threshold = 0
        self.txRate = 0
        self.txError = 0
        self.delay = 0
        self.jitter = 0
        self.packetLoss = 0
                
    def __str__(self):
        return str( self.movementType ) + "\t" + \
               str( self.threshold )  + "\t" + \
               str( self.txRate )  + "\t" + \
               str( self.txError ) + "\t" + \
               str( self.delay )  + "\t" + \
               str( self.jitter )  + "\t" + \
               str( self.packetLoss )