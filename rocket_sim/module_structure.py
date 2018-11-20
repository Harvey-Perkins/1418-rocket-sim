'''Structure that has no affect on the rocket except mass and aerodynamics (WIP)'''

import numpy as np

class Structure:
    mass = 0 #kg
    location = np.array([0.0,0.0,0.0]) #During setup, relative to the rocket origin, but during runtime relative to the CoM

    def update(self, t, dt):
        #Do nothing
        pass

    def __init__(self, mass):
        self.mass = mass
