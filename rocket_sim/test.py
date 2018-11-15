'''
This isn't permenant, just a demo of the velocity verlet and how it can calculate velocity and position from a acceleration vector.
In this case, it just simulates dropping an object from a certain height.
I think we will sum forces on the rocket, use the fact that F=MA to calculate the acceleration vector, then run that through the verlet.

Some thoughts on structure:
The simulated rocket is an object, with every part on it as something else, maybe another object?
All the parts should have modules for what they do. For example, the engines should have a mass and a thrust module
Probably we should use classes for most of this.
'''

import numpy as np
import scipy
import math
import module_engine as me

file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#file_path = "../data/load/thrustcurve/AeroTech_D21.rse"
#file_path = "../data/load/thrustcurve/AeroTech_H45.edx"
#file_path = "../data/load/thrustcurve/AeroTech_H125.txt"

#Testing class stuff
engine1 = me.Engine(file_path) #Create a new engine with the stats of a H45

#Simulates something falling 20 meters under gravity
#               x,y,z
g0 = np.array([0.0,0.0,-9.81])
position = np.array([0.0,0.0,20.0])
velocity = np.array([0.0,0.0,0.0])
t = 0
dt = 0.01

while position[2] > 0:
    t += dt
    position += velocity * dt + 0.5 * g0 *dt * dt #Just stealing this from someone else's implementation of the velocity verlet...
    velocity += g0 * dt
    if round(t, 10) == 0.1:
        engine1.ignite(0.1, t)
    engine1.update(t, dt)
    print("Time:")
    print(t)

print(t)


'''
#some random rotation tests
def rotation_matrix(axis, theta):
    #Returns rotation matrix describing counterclockwise rotation about the axis by theta radians
    #Stealing this from stackoverflow to check what the corrct result should be
    axis = np.asarray(axis) #converts axis to asarray type, which can be modified directly
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

v = [1, 1, 1]
axis = [1, 0, 0]
theta = math.radians(90) # original = 1.2

print(np.dot(rotation_matrix(axis, theta), v))
# [ 2.74911638  4.77180932  1.91629719]
'''
