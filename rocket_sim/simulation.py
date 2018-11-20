'''
This isn't permanant, just a demo of the velocity verlet and how it can calculate velocity and position from a acceleration vector.
In this case, it just simulates dropping an object from a certain height.
I think we will sum forces on the rocket, use the fact that F=MA (F/M = A) to calculate the acceleration vector, then run that through the verlet.

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


#               x,y,z
g0 = np.array([0.0,0.0,-9.81])
acc = np.array([0.0,0.0,0.0])
start_position = np.array([0.0,0.0,20.0])
start_velocity = np.array([0.0,0.0,0.0])
t = 0
dt = 0.01

xs = []#graph stuff
thrustY = []
ys = []

X = 0 #Makes accessing vector parts easier
Y = 1
Z = 2

rocket = mr.Rocket(start_position, start_velocity)
structure1 = ms.Structure(0.8)
engine1 = me.Engine(file_path, np.array([0,0,1]), 1000)
rocket.add_engine(engine1, np.array([0.0,0.0,-1.0]))
rocket.add_structure(structure1, np.array([0.0,0.0,0.0]))

#Graph stuff
fig, ax1 = plt.subplots()
ax1.set_ylabel("Altitude (m)")
ax1.set_xlabel("Time (s)")
ax2 = ax1.twinx()
ax2.set_ylabel("Thrust (N)")
fig.tight_layout()

while rocket.position[Z] > 0:
    #acc = np.array([0.0,0.0,0.0]) #reset acceleration
    #acc += g0 #add gravity to acceleration. Later sum all acceleration forces
    if round(t, 10) == 1.58: #Ignition command
        ax1.annotate('Ignition command', xy=(t, rocket.position[Z]), xytext=(2, 12),arrowprops=dict(facecolor='black', shrink=0)) #plots arrow pointing to when the ignition command is sent
        engine1.ignite(0.1, t)
    rocket.update(t, dt)

    rocket.position += rocket.velocity * dt + 0.5 * rocket.acceleration * dt * dt #Just stealing this from someone else's implementation of the velocity verlet...
    rocket.velocity += rocket.acceleration * dt

    #print(rocket.mass)
    #print(rocket.thrusts)

    xs.append(t)
    thrustY.append(np.linalg.norm(rocket.thrusts))
    ys.append(rocket.position[Z])

    t += dt

max = 0
for alt in ys:
    if alt >= max:
        max = alt

print("Max alt:")
print(max)

print(t)

ax1.plot(xs,ys)

ax2.plot(xs, thrustY)

plt.show()