'''
This should be a class that will be the entire rocket, with all the parts as sort of sub-pieces.



'''

import numpy as np

g0 = np.array([0.0,0.0,-9.81])

class Rocket:
    '''The main rocket class'''
    mass = 0 #sum of all nested object's masses
    position = np.array([0.0,0.0,0.0]) #Center of mass of the entire rocket
    velocity = np.array([0.0,0.0,0.0])
    acceleration = np.array([0,0,0])
    parts = []
    engines = []
    structures = []
    thrusts = np.array([0.0,0.0,0.0]) #sum of all (translational) forces on the rocket in N
    CoT = np.array([0.0,0.0,0.0]) #Center of thrust relative to rocket origin
    origin = np.array([0.0,0.0,0.0]) #Arbitrary origin location relative to the CoM

    def update(self, t, dt):
        self.acceleration = np.array([0.0,0.0,0.0])

        self.mass = 0
        self.thrusts = np.array([0.0,0.0,0.0])

        for part in self.parts:
            part.update(t, dt) #this ensures that only the rocket needs to be explictly updated in the main code
            self.mass += part.mass
        for engine in self.engines:
            self.thrusts += engine.thrust

        self.acceleration = self.thrusts/self.mass
        self.acceleration += g0

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_engine(self, part, location): #Location is relative to rocket origin
        #Call to add engines to the rocket
        self.engines.append(part)
        self.parts.append(part)
        part.location = location

    def add_structure(self, part, location):
        #Call to add structure to the rocket
        self.structures.append(part)
        self.parts.append(part)
        part.location = location
