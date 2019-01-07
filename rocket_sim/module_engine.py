# This modules should provide all the code needed for the engine

from data_converter import main
import random
import numpy as np


class Engine:
    '''The engine class'''

    ignition_delay = 0
    time_past_ignition = 0
    # some very large number
    fires_at = 10000000
    burning = False
    burnt_out = False
    curve = None  # This is an object
    # What way does the engine point, relative to the rocket? Unit vector
    thrust_vector = np.array([0, 0, 1])
    # Current thrust vector (non-unit), relative to the rocket
    thrust = np.array([0.0, 0.0, 0.0])
    dry_mass = 0  # empty mass
    wet_mass = 0  # Fully loaded mass
    mass = 0  # *Current* mass
    ve = 0  # Exhaust velocity
    m_dot = 0  # mass flow rate
    location = np.array([0.0, 0.0, 0.0])  # relative to the rocket origin
    comlocation = np.array([0.0, 0.0, 0.0])  # location relative to rocket CoM
    # location of center of thrust relative to engine's CoM (position)
    CoT = np.array([0.0, 0.0, 0.0])
    arm = np.array([0, 0, 0])  # Vector from rocket's CoM to engine's CoT
    # Torque vector for this specific engine relative to rocket
    torque = np.array([0, 0, 0])

    def update(self, t, dt):
        # Call every loop of the sim

        self.arm = self.comlocation + self.CoT  # Torque arm

        # Is the time past when it will start burning
        # and the engine is not yet burning?
        if t >= self.fires_at and not self.burning and not self.burnt_out:
            self.burning = True

        # Is the thrust curve function returning negative numbers
        # and the global time greater than the fires_at time?
        if self.curve(self.time_past_ignition) <= 0 and t > self.fires_at:
            self.burning = False
            self.burnt_out = True
            # That means the engine has burnt out
            self.thrust = np.array([0, 0, 0])
            self.mass = self.dry_mass
            self.m_dot = 0

        if self.burning and not self.burnt_out:  # Is the engine burning?
            # The engine has been burning for one more tick
            self.time_past_ignition += dt
            # mass only changes while the engine is burning
            self.thrust = self.curve(self.time_past_ignition) * self.thrust_vector
            # Mass flow rate in kg/s
            self.m_dot = np.linalg.norm(self.thrust)/self.ve
            # decrease the current mass appropiately
            self.mass -= self.m_dot * dt

        self.torque = np.cross(self.arm, self.thrust)
        # print("torque")
        # print(self.torque)

    def get_thrust(self, t, dt):
        if self.burning and not self.burnt_out:
            return self.curve(self.time_past_ignition) * self.thrust_vector
        else:
            return np.array([0, 0, 0])

    def ignite(self, delay, t):
        # Call when the ignition command is sent from the flight computer
        if delay == "random":
            # Put resonable values here later
            self.ignition_delay = random.randrange(1, 10, 1)/100
        else:
            self.ignition_delay = delay
        self.fires_at = t + self.ignition_delay  # It will fire at this time
        print("Ignition command sent")

    def __init__(self, file, vector, ve, CoT):
        # ve is required, but not used if it can be pulled from the files.
        # Otherwise just look up values
        # vector should be a array indicating the direction of the engine
        # CoT is relative to engine CoM (origin)
        self.curve = main.thrustcurve(file)  # Load thrust curve function
        self.CoT = CoT
        self.wet_mass = main.engine_mass(file)[0]
        # wet mass - prop mass = dry mass
        self.dry_mass = main.engine_mass(file)[0] - main.engine_mass(file)[1]
        self.mass = self.wet_mass  # engine starts loaded
        self.thrust_vector = vector
        if not is_number(main.engine_ve(file)):
            self.ve = ve
        else:
            self.ve = main.engine_ve(file)
        print(self.ve)
        print("Dry mass:")
        print(self.dry_mass)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
