'''
Converts RASP (.eng), RockSim (.rse), CompuRoc (.txt), and ALT4 (.edx) formats to list of x y pair lists.
NOTE: I am unsure of the units for thrust. Some may be lbs rather than N. Time should always be seconds though

Having the first data point 0,0 makes the cubic spline generator go wonky. So this also removes any points that are

TODO:
    Check thrust units.
'''
import os
import xml.etree.ElementTree as ET

'''
#This is for testing
script_dir = os.path.dirname(__file__)
#rel_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#rel_path = "../data/load/thrustcurve/AeroTech_D21.rse"
#rel_path = "../data/load/thrustcurve/AeroTech_H45.edx"
#rel_path = "../data/load/thrustcurve/AeroTech_H45.txt"
rel_path = "../data/load/thrustcurve/"
abs_path = os.path.join(script_dir, rel_path) #connects the path of where the file is being run, __file__, with the relative path of the data
file = open(abs_path)
'''


def converteng(file):
    #Returns list of lists [Seconds, Newtons]
    pair = [0,0]
    curve = []
    for line in file:
        if len(line.split()) > 2 or line[0] == ";": #checks if the line has more than one space, or is just a ;
            continue
        pair = [0,0]
        pair[0] = float(line.split()[0]) #time
        pair[1] = float(line.split()[1]) #thrust
        curve.append(pair)

    return curve

def convertrse(file):
    #returns list of lists [Seconds, Newtons]
    pair = [0,0]
    curve = []
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root[0][0].find("data"): #Searches for <data>
        pair = [0,0]
        if child.attrib["f"] == "0.":
            continue
        pair[0] = float(child.attrib["t"]) #time
        pair[1] = float(child.attrib["f"]) #thrust
        curve.append(pair)
    return curve

def convertedx(file):
    #return list of lists
    #Thust appears to be in lbf
    pair = [0,0]
    curve = []
    linenum = 0
    for line in file:
        pair = [0,0]
        if int(line.split()[0]) != 20: #checks that we're inside the thrust curve
            continue
        pair[0] = float(line.split("  ")[1].split()[2]) #splits on double space, then on single space. Time
        pair[1] = float(line.rsplit(" ", 1)[1].rstrip("\r\n")) * 4.4482216  #splits from right once, removes newline character. Converts from lbf to N
        curve.append(pair)
        ++linenum
    return curve

def convertcompuroc(file):
    #return list of lists
    pair = [0,0]
    curve = []
    for line in file:
        pair = [0,0]
        if line[0].isalpha() or line[0] == ";" or line[0] == "-": #checks that the line starts with a number, isn't a ;, and isn't negative
            continue
        if float(line.split()[0]) == 0:
            continue
        pair[0] = float(line.split()[0]) #time
        pair[1] = float(line.split()[1]) #thrust
        curve.append(pair)

    return curve
