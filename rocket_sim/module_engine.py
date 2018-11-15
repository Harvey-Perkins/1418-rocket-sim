#This modules should provide all the code needed for the engine

from data_converter import main

class Engine:
    '''The engine class'''

    def __init__(self, file):
        #Anything here is auto-run when the class is instantiated
        #Arguments can be passed along with self, such as the file name of the thrust curve to load
        self.curve = main.thrustcurve(file)
