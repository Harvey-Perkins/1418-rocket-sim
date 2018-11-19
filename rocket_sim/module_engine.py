#This modules should provide all the code needed for the engine

from data_converter import main
import random
import numpy as np

class Engine:
    '''The engine class'''

    ignition_delay = 0
    time_past_ignition = 0
    fires_at = 10000000 #some number that is longer than the number of seconds that will be simulated
    burning = False
    curve = None #This is an object
    thrust = 0
    dry_mass = 0 #empty mass
    wet_mass = 0 #Fully loaded mass
    mass = 0 #*Current* mass
    ve = 0
    m_dot = 0 #mass flow rate
    location = np.array([0.0,0.0,0.0]) #location relative to rocket origin

    def update(self, t, dt):
        #Call every loop of the sim
        if t >= self.fires_at: #Is the time past when it will start burning based on the ignition delay?
            self.burning = True

        if self.burning == True: #Is the engine burning?
            self.time_past_ignition += dt #The engine has been burning for one more tick
            #mass only changes while the engine is burning
            self.m_dot = self.thrust/self.ve #Mass flow rate in kg/s
            self.mass -= self.m_dot * dt #decrease the current mass appropiately

        if self.curve(self.time_past_ignition) <= 0 and t > self.fires_at: #Is the thrust curve function returning negative numbers?
            self.burning = False
            self.thrust = 0 #That means the engine has burnt out
            self.mass = self.dry_mass
            self.m_dot = 0
        else:
            self.thrust = self.curve(self.time_past_ignition) #Otherwise, just use the thrust curve function to determine the thrust

    def ignite(self, delay, t):
        #Call when the ignition command is sent from the flight computer
        if delay == "random":
            self.ignition_delay = random.randrange(1,10,1)/100 #Put resonable values here later
        else:
            self.ignition_delay = delay
        self.fires_at = t + self.ignition_delay #It will fire at this time
        print("Ignition command sent")


    def __init__(self, file, ve): #ve is required, but not used if it can be pulled from the files. Otherwise just look up values
        #Anything here is auto-run when the class is instantiated
        #Arguments can be passed along with self, such as the file name of the thrust curve to load
        self.curve = main.thrustcurve(file) #Load thrust curve function
        self.wet_mass = main.engine_mass(file)[0]
        self.dry_mass = main.engine_mass(file)[0] - main.engine_mass(file)[1] #wet mass - prop mass = dry mass
        self.mass = self.wet_mass #engine starts loaded
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
