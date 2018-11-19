'''Structure that has no affect on the rocket except mass and aerodynamics (WIP)'''

class Structure:
    mass = 0 #kg

    def update(self, t, dt):
        #Do nothing
        pass

    def __init__(self, mass):
        self.mass = mass
