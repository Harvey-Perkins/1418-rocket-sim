'''
This should be a class that will be the entire rocket,
with all the parts as sort of sub-pieces.
It updates everything else when it is updated

'''

import numpy as np

g0 = np.array([0.0, 0.0, -9.81])


class Rocket:
    '''The main rocket class'''
    mass = 0  # sum of all nested object's masses
    position = np.array([0.0, 0.0, 0.0])  # Global position of the rocket's CoM
    velocity = np.array([0.0, 0.0, 0.0])  # Global velocity of the rocket's CoM
    acceleration = np.array([0, 0, 0])
    xorientation = np.array([1.0, 0.0, 0.0])  # Global orientation vectors. Starts with no rotation, which means fire end towards ground, pointy end towards space
    yorientation = np.array([0.0, 0.0, 1.0])  # Wrong temporarily for testing vectors
    zorientation = np.array([0.0, -1.0, 0.0])  # THESE MAKE UP THE ROTATION MATRIX FOR THE ENTIRE ROCKET!!!
    xinertia = 0.08  # pitch or yaw. kg * m^2
    yinertia = 0.08  # pitch or yaw
    zinertia = 0.01  # roll
    # Using three values rather than a proper tensor only works in local coords, and only so long as the rocket is entirely symmetrical about the z axis with an angle less than 180.
    # Values are probably conpletely unreasonable
    # This is hopefully the right way to deal with inertia. These represent the diagonal of the moment of inertia tensor
    inertia = np.array([xinertia, yinertia, zinertia])  # I believe I can use the individual inertia parts, which are the diagonal of the tensor, as a vector to make some of the math easier.
    parts = []  # List of all parts in the rocket
    engines = []
    structures = []
    thrusts = np.array([0.0, 0.0, 0.0])  # sum of all (translational) forces on the rocket in N
    CoT = np.array([0.0, 0.0, 0.0])  # Center of thrust relative to rocket origin
    CoM = np.array([0.0, 0.0, 0.0])  # CoM relative to an arbitrary origin
    torques = np.array([0, 0, 0])  # Sum of torques on the rocket in Nm. Local coords
    torques_world = np.array([0, 0, 0])  # Sum or torques on the rocket, in world coords
    rot_matrix = np.array([xorientation, yorientation, zorientation])  # This might be wrong
    ang_momentum = np.array([0, 0, 0])  # local coords

    def update(self, t, dt):
        # reset
        self.acceleration = np.array([0.0, 0.0, 0.0])
        self.mass = 0
        self.thrusts = np.array([0.0, 0.0, 0.0])
        self.torques = np.array([0.0, 0.0, 0.0])

        for part in self.parts:
            # loop to update every part as necessary
            part.update(t, dt)  # this ensures that only the rocket needs to be explictly updated in the main code
            self.mass += part.mass
            partcomlocation(self, part)  # updates location relative to rocket com for all parts
        for engine in self.engines:
            # For things specific to engines, like thrust, torque, etc
            self.thrusts += engine.thrust
            self.torques += engine.torque
            self.torques_world = vectortoworld(self.torques, self.rot_matrix)

        self.acceleration = self.thrusts/self.mass
        self.acceleration += g0

        orthogonal(self)
        self.CoM = com_calc(self)

        self.rot_matrix = np.array([self.xorientation, self.yorientation, self.zorientation])  # Should I even update this here?

        '''print("x orientation")
        print(self.xorientation)
        print("y orientation")
        print(self.yorientation)
        print("z orientation")
        print(self.zorientation)'''

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_engine(self, part, location):  # Location is relative to rocket origin
        # Call to add engines to the rocket
        self.engines.append(part)
        self.parts.append(part)
        part.location = location

    def add_structure(self, part, location):
        # Call to add structure to the rocket
        self.structures.append(part)
        self.parts.append(part)
        part.location = location

# Object end


def vectortoworld(vector, matrix):
    # This turns local vectors into world vectors, based on the rotation matrix
    # Rotation matrix inverses are the same as their transposes
    return np.dot(np.transpose(matrix), vector)


def orthogonal(vehicle):
    # Sets orientation vectors orthogonal to each other
    x = vehicle.xorientation
    y = vehicle.yorientation
    z = vehicle.zorientation
    if (x != np.cross(y, z)).any() or (y != np.cross(z, x)).any() or (z != np.cross(x, y)).any():  # Weird syntax thanks to numpy handling boolean arrays weirdly
        print("Making orientation vectors orthogonal")
        # This isn't perfect, but it should be fine for handling small floating point errors
        vehicle.zorientation = np.cross(x, y)
        z = vehicle.zorientation
        vehicle.xorientation = np.cross(y, z)


def partcomlocation(vehicle, part):
    # calculates part's position relative to vehicle's CoM
    part.comlocation = part.location - vehicle.CoM


def com_calc(vehicle):
    # CoM position calc
    xcom = 0
    ycom = 0
    zcom = 0
    weightedsum = 0

    # Each of these loops calculates the com in one dimension
    for part in vehicle.parts:
        weightedsum += part.location[0] * part.mass  # X
    xcom = weightedsum / vehicle.mass

    weightedsum = 0
    for part in vehicle.parts:
        weightedsum += part.location[1] * part.mass  # Y
    ycom = weightedsum / vehicle.mass

    weightedsum = 0
    for part in vehicle.parts:
        weightedsum += part.location[2] * part.mass  # Z
    zcom = weightedsum / vehicle.mass

    return np.array([xcom, ycom, zcom])  # This just takes each one dimensional com and makes it into a 3d point
