#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                 P R E D I C T I O N   S A M P L E                            |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from operator import *
from Vector import Vector
from Sample import Sample

class PredictionSample(object):

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, *args):
        self.sample = Sample()
        self.velocity = Vector()
        
        if len(args) == 1:
            if isinstance( args[0], PredictionSample ):
                self.sample = copy( args[0].sample )
                self.velocity = copy( args[0].velocity )
        elif len(args) == 2:
            if isinstance( args[0], Sample ):
                self.sample = copy( args[0] )
            if isinstance( args[1], Vector ):
                self.velocity = copy( args[1] )
    
    def __str__(self):
        return str(self.sample) + "\t" + str(self.velocity)
    
    