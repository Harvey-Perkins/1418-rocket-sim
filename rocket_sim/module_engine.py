#This modules should provide all the code needed for the engine

from data_converter import main
import random

class Engine:
    '''The engine class'''

    ignition_delay = 0
    time_past_ignition = 0

    def ignite(self, delay):
        if delay == "random":
            self.ignition_delay = random.randrange(0.01,0.1,0.01) #Put resonable values here later
        else:
            self.ignition_delay = delay

    def __init__(self, file):
        #Anything here is auto-run when the class is instantiated
        #Arguments can be passed along with self, such as the file name of the thrust curve to load
        self.curve = main.thrustcurve(file)
        self.time_past_ignition = 0
