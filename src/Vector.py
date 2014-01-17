#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                             V E C T O R                                      |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from math import *

class Vector(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, *args):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        if len(args) == 1:
            if isinstance( args[0], Vector ):
                self.x = args[0].x
                self.y = args[0].y
                self.z = args[0].z
        elif len(args) == 3:
            if isinstance( args[0], float ) or isinstance( args[0], int ):
                self.x = args[0]
            if isinstance( args[1], float ) or isinstance( args[1], int ):    
                self.y = args[1]
            if isinstance( args[2], float ) or isinstance( args[2], int ):
                self.z = args[2]
            
    def __add__(self, otherVector):
        try:
            return Vector( self.x + otherVector.x, \
                           self.y + otherVector.y, \
                           self.z + otherVector.z)
        except AttributeError:
            print "Error: Other type must be Vector for vector addition."
            return self
        
    def __sub__(self, otherVector):
        try:
            return Vector( self.x - otherVector.x, \
                           self.y - otherVector.y, \
                           self.z - otherVector.z)
        except AttributeError:
            print "Error: Other type must be Vector for vector subtraction."
            return self
        
    def __mul__(self, otherVector):
        try:
            return Vector( self.x * float(otherVector.x), \
                           self.y * float(otherVector.y), \
                           self.z * float(otherVector.z))
        except:
            print "Error: Other type must be number for vector multiplication."
            return self
        
    def __div__(self, otherVector):
        try:
            return Vector( self.x / float(otherVector.x), \
                           self.y / float(otherVector.y), \
                           self.z / float(otherVector.z))
        except:
            print "Error: Other type must be number for vector division."
            return self
    
    def __str__(self):
        return str( self.x ) + "\t" + str( self.y ) + "\t" + str( self.z )
        
    def distance(self, otherVector):
        try:
            distance = ( otherVector.x - self.x )**2 + \
                       ( otherVector.y - self.y )**2 + \
                       ( otherVector.z - self.z )**2
            return sqrt(distance)
        except AttributeError:
            print "Error: Other type must be Vector for vector distance calculation."
            return self
        
    def magnitude(self):
        distance = ( self.x )**2 + ( self.y )**2 + ( self.z )**2
        return sqrt(distance)
    
    def abs(self):
        self.x = abs(self.x)
        self.y = abs(self.y)
        self.z = abs(self.z)
        return self