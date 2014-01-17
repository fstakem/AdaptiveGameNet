#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                    G L O B A L   V A R I A B L E S                           |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from enum import Enum

MovementType = Enum( 'Stacking', 'Catching', 'TieShoes')
TransmissionType = Enum( 'Synchronous', 'DR', 'AdaptiveDR' )
TestType = Enum( 'Delay', 'Jitter', 'DelayJitter' )