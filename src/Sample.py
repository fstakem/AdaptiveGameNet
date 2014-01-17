#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                             S A M P L E                                      |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from math import *
from Vector import Vector

class Sample(object):

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, *args):
        self.time = 0
        self.position = Vector()
        
        if len(args) == 1:
            if isinstance( args[0], Sample ):
                self.time = args[0].time
                self.position = copy( args[0].position )
        elif len(args) == 2:
            if isinstance( args[0], float ) or isinstance( args[0], int ):
                self.time = args[0]
            if isinstance( args[1], Vector ):
                self.position = copy( args[1] )         
        elif len(args) == 4:
            if isinstance( args[0], float ) or isinstance( args[0], int ):
                self.time = args[0]
            self.position = Vector( args[1], args[2], args[3] )
            
    def __str__(self):
        return str( self.time ) + "\t" + str(self.position)
                 
    def distance(self, otherSample):
        if isinstance( otherSample, Sample ):
            return self.position.distance(otherSample.position)
    
    