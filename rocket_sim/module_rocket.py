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
    parts = []

    def update(self):
        self.mass = 0
        for part in self.parts:
            self.mass += part.mass

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_part(self, part):
        #Call to add parts to the rocket
        self.parts.append(part)
