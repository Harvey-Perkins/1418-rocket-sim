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
    thrust = 0
    dry_mass = 0 #This is going to be a bit of a challenge
    wet_mass = 0
    mass = 0

    def update(self, t, dt):
        #Call every loop of the sim
        if t >= self.fires_at: #Is the time past when it will start burning based on the ignition delay?
            self.burning = True

        if self.burning == True: #Is the engine burning?
            self.time_past_ignition += dt #The engine has been burning for one more tick

        if self.curve(self.time_past_ignition) <= 0: #Is the thrust curve function returning negative numbers?
            self.burning = False
            self.thrust = 0 #That means the engine has burnt out
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


    def __init__(self, file):
        #Anything here is auto-run when the class is instantiated
        #Arguments can be passed along with self, such as the file name of the thrust curve to load
        self.curve = main.thrustcurve(file) #Load thrust curve function
