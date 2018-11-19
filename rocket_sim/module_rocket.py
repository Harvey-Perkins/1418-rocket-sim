'''
This should be a class that will be the entire rocket, with all the parts as sort of sub-pieces.
Will need some kind of local coord system
The problem is the the CoM is what is simulated, but right now it's set up for the CoM to be apart from what the simulated center is

'''

import numpy as np

class Rocket:
    '''The main rocket class'''
    mass = 0 #sum of all nested object's masses
    position = np.array([0.0,0.0,0.0]) #Center of mass of the entire rocket
    velocity = np.array([0.0,0.0,0.0])
    parts = []
    thrusts = np.array([0.0,0.0,0.0]) #sum of all (translational) forces on the rocket in N
    CoT = np.array([0.0,0.0,0.0]) #Center of thrust relative to rocket origin
    origin = np.array([0.0,0.0,0.0]) #Arbitrary origin location relative to the CoM

    def update(self, t, dt):
        self.mass = 0
        for part in self.parts:
            part.update(t, dt) #this ensures that only the rocket needs to be explictly updated in the main code
            self.mass += part.mass

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_part(self, part, location): #Location is relative to rocket origin
        #Call to add parts to the rocket
        self.parts.append(part)
        part.location = location
