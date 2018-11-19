'''Structure that has no affect on the rocket except mass and aerodynamics (WIP)'''

import numpy as np

class Structure:
    mass = 0 #kg
    location = np.array([0.0,0.0,0.0]) #Location relative to rocket origin

    def update(self, t, dt):
        #Do nothing
        pass

    def __init__(self, mass):
        self.mass = mass
