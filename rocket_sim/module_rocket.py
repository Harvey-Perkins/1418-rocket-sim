'''
This should be a class that will be the entire rocket,
with all the parts as sort of sub-pieces.
It updates everything else when it is updated
TODO:
t + dt updates to rotation stuff

'''

import numpy as np
import math

g0 = np.array([0.0, 0.0, -9.81])  # 0,0,-9.81


class Rocket:
    '''The main rocket class'''
    mass = 0  # sum of all nested object's masses
    position = np.array([0.0, 0.0, 0.0])  # Global position of the rocket's CoM
    velocity = np.array([0.0, 0.0, 0.0])  # Global velocity of the rocket's CoM
    velocity_world = np.array([0.0, 0.0, 0.0])  # local velocity
    accel = np.array([0, 0, 0])  # in local coords
    accel_tpdt = np.array([0, 0, 0])  # at t + dt
    accel_world = np.array([0, 0, 0])  # in world coords
    accel_tpdt_world = np.array([0, 0, 0])  # in world coords
    # Global orientation vectors.
    # Starts with no rotation, which means fire end towards ground,
    # pointy end towards space
    # These are never used/updated after initializing the rotation matrix
    xorientation = np.array([1.0, 0.0, 0.0])
    yorientation = np.array([0.0, 1.0, 0.0])
    zorientation = np.array([0.0, 0.0, 1.0])
    # Using three values rather than a proper tensor only works in local coords
    # and only so long as the rocket is entirely symmetrical about the z axis
    # Values are probably conpletely unreasonable
    # These represent the diagonal of the moment of inertia tensor
    xinertia = 0.08  # pitch or yaw. kg * m^2
    yinertia = 0.08  # pitch or yaw
    zinertia = 0.01  # roll
    # As a vector
    inertia = np.array([xinertia, yinertia, zinertia])
    parts = []  # List of all parts in the rocket
    engines = []
    structures = []
    # sum of all (translational) forces on the rocket in N
    thrusts = np.array([0.0, 0.0, 0.0])
    thrusts_tpdt = np.array([0.0, 0.0, 0.0])  # at time t + dt
    # Center of thrust relative to rocket origin
    CoT = np.array([0.0, 0.0, 0.0])
    CoM = np.array([0.0, 0.0, 0.0])  # CoM relative to an arbitrary origin
    # Sum of torques on the rocket in Nm. Local coords
    torques = np.array([0, 0, 0])
    torques_tpdt = np.array([0, 0, 0])  # For use after time update
    rot_matrix = np.array([xorientation, yorientation, zorientation])
    ang_momentum = np.array([0, 0, 0])  # local coords
    ang_velocity = np.array([0, 0, 0])
    ang_delta_local = np.array([0, 0, 0])
    ang_delta_world = np.array([0, 0, 0])

    def update(self, t, dt):
        # reset
        self.accel = np.array([0.0, 0.0, 0.0])
        self.accel_world = np.array([0.0, 0.0, 0.0])
        self.accel_tpdt = np.array([0.0, 0.0, 0.0])
        self.accel_tpdt_world = np.array([0.0, 0.0, 0.0])
        self.mass = 0
        self.thrusts = np.array([0.0, 0.0, 0.0])
        self.thrusts_tpdt = np.array([0.0, 0.0, 0.0])
        self.torques = np.array([0.0, 0.0, 0.0])
        self.torques_tpdt = np.array([0.0, 0.0, 0.0])

        for part in self.parts:
            # loop to update every part as necessary
            part.update(t, dt)
            self.mass += part.mass

        self.CoM = com_calc(self)

        for part in self.parts:
            # updates location relative to rocket com for all parts
            # seperate loop so the rocket CoM is accurate
            partcomlocation(self, part)

        for engine in self.engines:
            # For things specific to engines, like thrust, torque, etc
            self.thrusts += engine.thrust
            self.torques += engine.torque

        # Compute acceleration
        self.accel = self.thrusts/self.mass
        # add gravity
        self.accel += vectortolocal(g0, self.rot_matrix)
        self.accel_world = vectortoworld(self.accel, self.rot_matrix)

        # main update
        # Done in world coords
        self.position += self.velocity_world * dt + 0.5 * self.accel_world * dt * dt

        self.ang_velocity = self.ang_momentum / self.inertia
        self.ang_delta_local = self.ang_velocity * dt + 0.5 * dt * dt * self.torques / self.inertia
        self.ang_delta_world = vectortoworld(
                                            self.ang_delta_local,
                                            self.rot_matrix)
        # Not sure if this should be multiplied from left or right
        # self.rot_matrix = np.matmul(self.rot_matrix, rodrigues(self.ang_delta_world))
        self.rot_matrix = np.matmul(rodrigues(self.ang_delta_world), self.rot_matrix)
        # matmul is a preliminary feature in numpy
        # print(self.velocity_world)
        # print(self.accel_world)
        # print(self.ang_velocity)
        # print(self.rot_matrix)

        t += dt  # this is not the main time update, it's only used here

        # compute forces at time time t + dt
        for engine in self.engines:
            # this is the t + dt version
            # For things specific to engines, like thrust, torque, etc
            self.thrusts_tpdt += engine.get_thrust(t, dt)
            self.torques_tpdt += engine.get_torque(t, dt)

        # compute acceleration at time t + dt
        self.accel_tpdt = self.thrusts_tpdt/self.mass
        # add gravity
        self.accel_tpdt += vectortolocal(g0, self.rot_matrix)
        self.accel_tpdt_world = vectortoworld(self.accel_tpdt, self.rot_matrix)

        '''print("accel:")
        print(self.accel)
        print("accel_tpdt:")
        print(self.accel_tpdt)'''

        # Better velocity calc
        self.velocity_world += 0.5 * (self.accel_world + self.accel_tpdt_world) * dt
        self.velocity = vectortolocal(self.velocity_world, self.rot_matrix)

        self.ang_momentum = self.ang_momentum + 0.5 * (self.torques + self.torques_tpdt) * dt

        self.rot_matrix = orthogonal(self.rot_matrix)

        '''print("x orientation")
        print(self.xorientation)
        print("y orientation")
        print(self.yorientation)
        print("z orientation")
        print(self.zorientation)'''

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def add_engine(self, part, location):
        # Location is relative to rocket origin
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


def vectortolocal(vector, matrix):
    # This turns world vectors into local vectors, based on the rotation matrix
    # Rotation matrix inverses are the same as their transposes
    return np.dot(matrix, vector)


def orthogonal(matrix):
    # Sets orientation vectors orthogonal to each other
    x = np.split(matrix, 3)[0][0]
    y = np.split(matrix, 3)[1][0]
    z = np.split(matrix, 3)[2][0]

    if (x != np.cross(y, z)).any() or (y != np.cross(z, x)).any() or (z != np.cross(x, y)).any():
        # Weird syntax thanks to numpy handling boolean arrays weirdly
        print("Making orientation vectors orthogonal")
        # This should be fine for handling floating point errors
        z = np.cross(x, y)
        x = np.cross(y, z)

    return np.array([x, y, z])


def rodrigues(ang_delta):
    # Rodrigues' rotation forumla.
    # Takes a vector describing the angle the vehicle rotates by in a tick
    # returns the rotation matrix for rotation around the axis of the vector
    # by the magnitude of the vector.
    axis = normalize(ang_delta)
    # print(axis)
    # The way angles (radians or degrees) work here might be wrong
    angle = np.linalg.norm(ang_delta)
    # print(angle)
    a = math.cos(angle/2)
    b = -axis[0] * math.sin(angle/2)
    c = -axis[1] * math.sin(angle/2)
    d = -axis[2] * math.sin(angle/2)
    '''a = angle
    b = -axis[0] * angle
    c = -axis[1] * angle
    d = -axis[2] * angle'''
    # I don't think this can be made any more readable
    return np.array([
                    [a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c)],
                    [2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
                    [2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c]])


def normalize(vector):
    # Normalizes (extracts the unit vector in) any vector
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


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

    # This just takes each one dimensional com and makes it into a 3d point
    return np.array([xcom, ycom, zcom])
