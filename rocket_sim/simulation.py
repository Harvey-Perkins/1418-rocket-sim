'''
TODO:
Make a proper test setup for this program

Moment of inertia
'''

import numpy as np
# import scipy
# import math
import module_engine as me
import module_rocket as mr
import module_structure as ms
import matplotlib.pyplot as plt
import vpython as vp
import time

# file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
file_path = "../data/load/thrustcurve/AeroTech_D21.rse"
# file_path = "../data/load/thrustcurve/AeroTech_H45.edx"
# file_path = "../data/load/thrustcurve/AeroTech_H125.txt"


#               x,y,z
g0 = np.array([0.0, 0.0, -9.81])
acc = np.array([0.0, 0.0, 0.0])
start_position = np.array([0.0, 0.0, 100.0])
start_velocity = np.array([0.0, 0.0, 0.0])
t = 0
dt = 0.01
counter = 0
xs = []  # graph stuff
thrustY = []
ys = []

X = 0  # Makes accessing vector parts easier
Y = 1
Z = 2

# Initialize parts
rocket = mr.Rocket(start_position, start_velocity)
structure1 = ms.Structure(0.0736)
engine1 = me.Engine(file_path,
                    np.array([0, 0, 1]),
                    1000,
                    np.array([0, 0, 0.05]))
engine2 = me.Engine(file_path,
                    np.array([0, 0, -1]),
                    1000,
                    np.array([0, 0, 0.05]))
# Stick them on the rocket
# rocket.add_engine(engine1, np.array([1, 0, -1.0]))
rocket.add_engine(engine1, np.array([1, 0, 0]))
rocket.add_engine(engine2, np.array([-1, 0, 0]))
rocket.add_structure(structure1, np.array([0.0, 0.0, 0.0]))

# Graph stuff
fig, ax1 = plt.subplots()
ax1.set_ylabel("Altitude (m)")
ax1.set_xlabel("Time (s)")
ax2 = ax1.twinx()
ax2.set_ylabel("Thrust (N)")
fig.tight_layout()

location = vp.sphere(pos=vp.vector(0,100,0))
orientation = vp.arrow(pos=vp.vector(10,0,0), axis=vp.vector(0,1,0))
center = vp.sphere(pos=vp.vector(0,0,0))
rocket_zorientation = np.array([0,0,0])

while rocket.position[Z] >= 0 and rocket.position[Z] < 200:
    # VPython stuff
    location.pos = vp.vector(rocket.position[X],
                        rocket.position[Z],
                        rocket.position[Y])
    rocket_zorientation = np.split(rocket.rot_matrix, 3)[2][0]
    orientation.axis = 10 * vp.vector(rocket_zorientation[X],
                            rocket_zorientation[Z],
                            rocket_zorientation[Y])
    print(rocket.velocity_world)
    time.sleep(0.01)

    counter += 1
    if counter >= 1000:
        rocket.position[Z] = -1
    # print(rocket.rot_matrix)
    '''print("Torque vector local:")
    print(rocket.torques)
    print("Torque vector world:")
    print(rocket.torques_world)'''
    if rocket.position[Z] == 100:  # Ignition command
        # plots arrow pointing to when the ignition command is sent
        ax1.annotate(
            'Ignition command',
            xy=(t, rocket.position[Z]), xytext=(2, 12),
            arrowprops=dict(facecolor='black', shrink=0))
        engine1.ignite(0, t)  # Ignition command
        engine2.ignite(0, t)
    rocket.update(t, dt)

    # print(rocket.mass)
    # print(rocket.thrusts)

    # Graphing stuff
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

ax1.plot(xs, ys)

ax2.plot(xs, thrustY)

plt.show()
