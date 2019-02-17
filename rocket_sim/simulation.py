'''
TODO:
Make a proper test setup for this program

'''

import numpy as np
# import scipy
# import math
import module_engine as me
import module_rocket as mr
import module_structure as ms
import matplotlib.pyplot as plt

import time
from appJar import gui

# file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
file_path = "../data/load/thrustcurve/AeroTech_D21.rse"
# file_path = "../data/load/thrustcurve/AeroTech_H45.edx"
# file_path = "../data/load/thrustcurve/AeroTech_H125.txt"


#               x,y,z
g0 = np.array([0.0, 0.0, -9.81])
acc = np.array([0.0, 0.0, 0.0])
start_position = np.array([0.0, 0.0, 100.0])  # set by user
start_velocity = np.array([0.0, 0.0, 0.0])
visualization = False  # set by user
graph = True  # set by user
t = 0
dt = 0.01  # set by user
delay = 0.01  # set by user, delay in animation
counter = 0
xs = []  # graph stuff
thrustY = []
ys = []

structure1 = True
structure1mass = 0.0736  # user editable
# user editable, relative to rocket engine
structure1location = np.array([0.0, 0.0, 0.0])

X = 0  # Makes accessing vector parts easier
Y = 1
Z = 2


# gui based rocket construction
setup = gui()
setup.addLabel("Title", "Setup")


def confirm():
    global visualization
    global start_position
    global graph
    global dt
    global delay
    global structure1
    global structure1mass
    global structure1location
    visualization = setup.getCheckBox("Visualization")
    graph = setup.getCheckBox("Graph")
    dt = float(setup.getEntry("Physics delta time"))
    delay = float(setup.getEntry("Visualization speed"))
    start_position = np.array([
        float(setup.getEntry("start_X")),
        float(setup.getEntry("start_Y")),
        float(setup.getEntry("start_Z"))])

    structure1 = setup.getCheckBox("Structure 1")
    structure1mass = float(setup.getEntry("Structure 1 mass"))
    structure1location = np.array([
        float(setup.getEntry("st1_loc_X")),
        float(setup.getEntry("st1_loc_Y")),
        float(setup.getEntry("st1_loc_Z"))
    ])
    setup.stop()


def nothing():
    setup.stop()
    # This is so the values set inside the code itself can be used quickly


setup.startTabbedFrame("Setup")

# first tab is for sim
setup.startTab("Simulation")
setup.addCheckBox("Visualization")
setup.addCheckBox("Graph")
setup.addLabelEntry("Physics delta time")
setup.setEntry("Physics delta time", 0.01)
setup.setEntryTooltip("Physics delta time", "Simulation precision")
setup.addLabelEntry("Visualization speed")
setup.setEntry("Visualization speed", 0.01)
setup.setEntryTooltip(
    "Visualization speed",
    "How fast the animation runs, set same as delta time for near real time")
setup.stopTab()

# 2nd tab is for rocket setup
setup.startTab("Rocket")
setup.addLabel("Start Position")
setup.addLabelEntry("start_X")
setup.addLabelEntry("start_Y")
setup.addLabelEntry("start_Z")
setup.setEntry("start_X", 0)
setup.setEntry("start_Y", 0)
setup.setEntry("start_Z", 0)
setup.stopTab()

# structures
setup.startTab("Structures")
setup.addCheckBox("Structure 1")
setup.setCheckBox("Structure 1", True)
setup.addLabelEntry("Structure 1 mass")
setup.setEntry("Structure 1 mass", 0.0736)
setup.addLabel("Structure 1 location (relative to origin)")
setup.addLabelEntry("st1_loc_X")
setup.addLabelEntry("st1_loc_Y")
setup.addLabelEntry("st1_loc_Z")
setup.setEntry("st1_loc_X", 0)
setup.setEntry("st1_loc_Y", 0)
setup.setEntry("st1_loc_Z", 0)
setup.stopTab()

# Next tab is for engines
setup.startTab("Engines")
setup.stopTab()
# Last tab is for inflight events
setup.startTab("Inflight")
setup.stopTab()

setup.stopTabbedFrame()

setup.addButton("Confirm", confirm)
setup.addButton("Debug continue", nothing)

setup.go()


# Initialize parts
rocket = mr.Rocket(start_position, start_velocity)
if structure1:
    structure1 = ms.Structure(structure1mass)
    rocket.add_structure(structure1, structure1location)

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

# Graph
if graph:
    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Altitude (m)")
    ax1.set_xlabel("Time (s)")
    ax2 = ax1.twinx()
    ax2.set_ylabel("Thrust (N)")
    fig.tight_layout()

# Visualization
if visualization:
    import vpython as vp
    location = vp.sphere(pos=vp.vector(0, 100, 0))
    orientation = vp.arrow(pos=vp.vector(10, 0, 0), axis=vp.vector(0, 1, 0))
    center = vp.sphere(pos=vp.vector(0, 0, 0))
    rocket_zorientation = np.array([0, 0, 0])

while rocket.position[Z] >= 0 and rocket.position[Z] < 200:
    # VPython stuff
    if visualization:
        location.pos = vp.vector(
                            rocket.position[X],
                            rocket.position[Z],
                            rocket.position[Y])
        rocket_zorientation = np.split(rocket.rot_matrix, 3)[2][0]
        orientation.axis = 10 * vp.vector(
                                rocket_zorientation[X],
                                rocket_zorientation[Z],
                                rocket_zorientation[Y])
        # print(rocket.velocity_world)
        time.sleep(delay)

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
        if graph:
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

# graph
if graph:
    ax1.plot(xs, ys)
    ax2.plot(xs, thrustY)
    plt.show()
