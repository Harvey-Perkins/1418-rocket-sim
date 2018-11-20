'''
This should be a class that will be the entire rocket, with all the parts as sort of sub-pieces.

TODO:
Make the parts' locations relative to the CoM during runtime

'''

import numpy as np

g0 = np.array([0.0,0.0,-9.81])

class Rocket:
    '''The main rocket class'''
    mass = 0 #sum of all nested object's masses
    position = np.array([0.0,0.0,0.0]) #Global position of the rocket
    velocity = np.array([0.0,0.0,0.0])
    acceleration = np.array([0,0,0])
    parts = []
    engines = []
    structures = []
    thrusts = np.array([0.0,0.0,0.0]) #sum of all (translational) forces on the rocket in N
    CoT = np.array([0.0,0.0,0.0]) #Center of thrust relative to rocket origin
    CoM = np.array([0.0,0.0,0.0]) #CoM relative to an arbitrary origin


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

        self.CoM = com_calc(self)

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_engine(self, part, location): #Location is relative to rocket origin when added, but is changed during runtime to be relative to the CoM
        #Call to add engines to the rocket
        self.engines.append(part)
        self.parts.append(part)
        part.location = location

    def add_structure(self, part, location):
        #Call to add structure to the rocket
        self.structures.append(part)
        self.parts.append(part)
        part.location = location

def com_calc (vehicle):
    #CoM position calc
    xcom = 0
    ycom = 0
    zcom = 0
    weightedsum = 0

    #CoM position calc
    #Each of these loops calculates the com in one dimension
    for part in vehicle.parts:
        weightedsum += part.location[0] * part.mass #X
    xcom = weightedsum / vehicle.mass

    weightedsum = 0
    for part in vehicle.parts:
        weightedsum += part.location[1] * part.mass #Y
    ycom = weightedsum / vehicle.mass

    weightedsum = 0
    for part in vehicle.parts:
        weightedsum += part.location[2] * part.mass #Z
    zcom = weightedsum / vehicle.mass

    return np.array([xcom,ycom,zcom]) #This just takes each one dimensional com and makes it into a 3d point
