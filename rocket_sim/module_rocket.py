'''
This should be a class that will be the entire rocket, with all the parts as sort of sub-pieces.
Will need some kind of local coord system

'''

import numpy as np

class Rocket:
    '''The main rocket class'''
    mass = 0 #sum of all nested object's masses
    position = np.array([0.0,0.0,0.0])
    velocity = np.array([0.0,0.0,0.0])

    def __init__(self, position, velocity):
        '''Probably will add parts?'''
        self.position = position
        self.velocity = velocity
