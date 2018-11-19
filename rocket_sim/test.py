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
import module_rocket as mr
import module_structure as ms
import matplotlib.pyplot as plt

#file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
file_path = "../data/load/thrustcurve/AeroTech_D21.rse"
#file_path = "../data/load/thrustcurve/AeroTech_H45.edx"
#file_path = "../data/load/thrustcurve/AeroTech_H125.txt"

#Testing class stuff
 #Create a new engine with the thrust curve of whatever engine

#Simulates something falling 20 meters under gravity
#               x,y,z
g0 = np.array([0.0,0.0,-9.81])
acc = np.array([0.0,0.0,0.0])
start_position = np.array([0.0,0.0,20.0])
start_velocity = np.array([0.0,0.0,0.0])
t = 0
dt = 0.01

xs = []#graph stuff
ys = []

X = 0 #Makes accessing vector parts easier
Y = 1
Z = 2

rocket = mr.Rocket(start_position, start_velocity)
structure1 = ms.Structure(1)
engine1 = me.Engine(file_path, 1000)
rocket.add_part(engine1, np.array([0.0,0.0,-1.0]))
rocket.add_part(structure1, np.array([0.0,0.0,0.0]))

while rocket.position[Z] > 0:
    acc = np.array([0.0,0.0,0.0]) #reset acceleration
    acc += g0 #add gravity to acceleration. Later sum all acceleration forces
    t += dt
    rocket.position += rocket.velocity * dt + 0.5 * acc * dt * dt #Just stealing this from someone else's implementation of the velocity verlet...
    rocket.velocity += acc * dt
    if round(t, 10) == 0.1: #Ignition command
        engine1.ignite(0.1, t)
    rocket.update(t, dt)

    print(rocket.mass)

    xs.append(t)
    ys.append(rocket.position[Z])

print(t)
plt.plot(xs,ys)
plt.show()


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
