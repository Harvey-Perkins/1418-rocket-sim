'''
This should be a class that will be the entire rocket, with all the parts as sort of sub-pieces.

'''

import numpy as np

g0 = np.array([0.0,0.0,-9.81])

class Rocket:
    '''The main rocket class'''
    mass = 0 #sum of all nested object's masses
    position = np.array([0.0,0.0,0.0]) #Global position of the rocket's CoM
    velocity = np.array([0.0,0.0,0.0]) #Global velocity of the rocket's CoM
    acceleration = np.array([0,0,0])
    xorientation = np.array([1.0,0.0,0.0]) #Global orientation vectors. Starts with no rotation, which means fire end towards ground, pointy end towards space
    yorientation = np.array([0.0,1.0,0.0])
    zorientation = np.array([0.0,0.0,1.0])
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
            #loop to update every part as necessary
            part.update(t, dt) #this ensures that only the rocket needs to be explictly updated in the main code
            self.mass += part.mass
            partcomlocation(self, part)
        for engine in self.engines:
            self.thrusts += engine.thrust

        self.acceleration = self.thrusts/self.mass
        self.acceleration += g0

        orthogonal(self)
        self.CoM = com_calc(self)
        print("x orientation")
        print(self.xorientation)
        print("y orientation")
        print(self.yorientation)
        print("z orientation")
        print(self.zorientation)

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_engine(self, part, location, CoT): #Location is relative to rocket origin, CoT is relative to engine CoM (origin)
        #Call to add engines to the rocket
        self.engines.append(part)
        self.parts.append(part)
        part.location = location
        part.CoT = CoT

    def add_structure(self, part, location):
        #Call to add structure to the rocket
        self.structures.append(part)
        self.parts.append(part)
        part.location = location

def orthogonal (vehicle):
    #Sets orientation vectors orthogonal to each other
    x = vehicle.xorientation
    y = vehicle.yorientation
    z = vehicle.zorientation
    if (x != np.cross(y, z)).any() or (y != np.cross(z, x)).any() or (z != np.cross(x, y)).any(): #Weird syntax thanks to numpy handling boolean arrays weirdly
        print("Making orientation vectors orthogonal")
        vehicle.zorientation = np.cross(x, y) #This isn't perfect, but it should be fine for handling small floating point errors
        z = vehicle.zorientation
        vehicle.xorientation = np.cross(y, z)

def partcomlocation (vehicle, part):
    #calculates part's position relative to vehicle's CoM
    part.comlocation = part.location - vehicle.CoM

def com_calc (vehicle):
    #CoM position calc
    xcom = 0
    ycom = 0
    zcom = 0
    weightedsum = 0

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
