'''
This isn't permanant, just a demo of the velocity verlet and how it can calculate velocity and position from a acceleration vector.
In this case, it just simulates dropping an object from a certain height.
I think we will sum forces on the rocket, use the fact that F=MA to calculate the acceleration vector, then run that through the verlet.

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
    print(engine1.thrust)

    xs.append(t)
    ys.append(rocket.position[Z])

print(t)
plt.plot(xs,ys)
plt.show()
