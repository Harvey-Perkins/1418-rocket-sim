'''
TODO:
Close the file after I'm done with it
'''

from data_converter import convert
import os
from data_converter import curve_gen
from data_converter import mass
from data_converter import isp

#file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#file_path = "../data/load/thrustcurve/AeroTech_D21.rse"
#file_path = "../data/load/thrustcurve/AeroTech_H45.edx"
#file_path = "../data/load/thrustcurve/AeroTech_H125.txt"


def thrustcurve(rel_path):
    #rel_path should be a file path in the format of the examples above
    #returns either a cubic spline function or a bezier object
    script_dir = os.path.dirname(__file__)
    abs_path = os.path.join(script_dir, rel_path) #connects the path of where the file is being run, __file__, with the relative path of the data
    file = open(abs_path, "r")

    #print(file.name.rsplit("/",1)[1]) #debug
    if file.name.rsplit("/", 1)[1] == "00INDEX.txt": #Ignores index
        #do nothing
        print("That's the index")
    elif file.name.rsplit(".", 1)[1] == "eng": #detects file extension
        return curve_gen.cubiccurve(convert.converteng(file))
    elif file.name.rsplit(".", 1)[1] == "rse":
        return curve_gen.cubiccurve(convert.convertrse(file))
    elif file.name.rsplit(".", 1)[1] == "edx":
        return curve_gen.cubiccurve(convert.convertedx(file))
    elif file.name.rsplit(".", 1)[1] == "txt":
        return curve_gen.cubiccurve(convert.convertcompuroc(file))

def engine_mass(rel_path):
    #Calls mass.py
    #Returns output of mass readers directly, should always be in [wet mass, prop mass] form in kg
    script_dir = os.path.dirname(__file__)
    abs_path = os.path.join(script_dir, rel_path) #connects the path of where the file is being run, __file__, with the relative path of the data
    file = open(abs_path, "r")

    if file.name.rsplit("/", 1)[1] == "00INDEX.txt": #Ignores index
        #do nothing
        print("That's the index")
    elif file.name.rsplit(".", 1)[1] == "eng": #detects file extension
        return mass.mass_eng(file)
    elif file.name.rsplit(".", 1)[1] == "rse":
        return mass.mass_rse(file)
    elif file.name.rsplit(".", 1)[1] == "edx":
        return mass.mass_edx(file)
    elif file.name.rsplit(".", 1)[1] == "txt":
        return mass.mass_txt(file)

def engine_ve(rel_path):
    #Calls isp.py
    #Returns output of isp.py directly, in units of m/s
    script_dir = os.path.dirname(__file__)
    abs_path = os.path.join(script_dir, rel_path) #connects the path of where the file is being run, __file__, with the relative path of the data
    file = open(abs_path, "r")

    if file.name.rsplit("/", 1)[1] == "00INDEX.txt": #Ignores index
        #do nothing
        print("That's the index")
    elif file.name.rsplit(".", 1)[1] == "eng": #detects file extension
        return "No ve in that format. Look up the isp/ve for the engine and plug it in manually."
    elif file.name.rsplit(".", 1)[1] == "rse":
        return isp.ve_rse(file)
    elif file.name.rsplit(".", 1)[1] == "edx":
        return isp.ve_edx(file)
    elif file.name.rsplit(".", 1)[1] == "txt":
        return "No ve in that format. Look up the isp/ve for the engine and plug it in manually"

#print(engine_mass(file_path))
#print(engine_ve(file_path))
#thrustcurve(file_path) #debug
