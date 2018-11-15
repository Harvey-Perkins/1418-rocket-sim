from data_converter import convert
import os
from data_converter import curve_gen

#file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#file_path = "../data/load/thrustcurve/Estes_D12.rse"
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
        print()
    elif file.name.rsplit(".", 1)[1] == "eng": #detects file extension
        return curve_gen.cubiccurve(convert.converteng(file))
    elif file.name.rsplit(".", 1)[1] == "rse":
        return curve_gen.cubiccurve(convert.convertrse(file))
    elif file.name.rsplit(".", 1)[1] == "edx":
        return curve_gen.cubiccurve(convert.convertedx(file))
    elif file.name.rsplit(".", 1)[1] == "txt":
        return curve_gen.cubiccurve(convert.convertcompuroc(file))

#thrustcurve(file_path) #debug
