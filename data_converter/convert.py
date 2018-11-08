'''
Converts RASP (.eng), RockSim (.rse), CompuRoc (.txt), and ALT4 (.edx) formats to... somthing. Not exactly sure what yet.
'''
import os

script_dir = os.path.dirname(__file__)
rel_path = "../data/load/thrustcurve/AeroTech_D10.eng"
abs_path = os.path.join(script_dir, rel_path)

file = open(abs_path, "r")
#print(file.read())

def converteng(file):
    #Returns list of lists
    time = 0.0
    thrust = 0.0
    pair = [0,0]
    curve = []
    for line in file:
        if line[0].isalpha():
            continue
        print(line)
        pair[0] = line.split()[0]
        pair[1] = line.split()[1]
        print(pair)
        curve.append(pair)
        print(curve) #Why won't this work?

    return curve

print(converteng(file))
