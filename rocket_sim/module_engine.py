#This modules should provide all the code needed for the engine

from data_converter import main
import random

class Engine:
    '''The engine class'''

    ignition_delay = 0
    time_past_ignition = 0
    fires_at = 10000000 #some number that is longer than the number of seconds that will be simulated
    burning = False
    curve = None #This is an object

    def update(self, t, dt):
        #Call every loop of the sim
        if t >= self.fires_at:
            self.burning = True

        if self.burning == True:
            self.time_past_ignition += dt

    def ignite(self, delay, t):
        if delay == "random":
            self.ignition_delay = random.randrange(1,10,1)/100 #Put resonable values here later
        else:
            self.ignition_delay = delay
        self.fires_at = t + self.ignition_delay
        print("Ignition command sent")


    def __init__(self, file):
        #Anything here is auto-run when the class is instantiated
        #Arguments can be passed along with self, such as the file name of the thrust curve to load
        self.curve = main.thrustcurve(file)
