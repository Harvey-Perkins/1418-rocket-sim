'''
Converts RASP (.eng), RockSim (.rse), CompuRoc (.txt), and ALT4 (.edx) formats to... somthing. Not exactly sure what yet.
'''
import os
import xml.etree.ElementTree as ET

script_dir = os.path.dirname(__file__)
#rel_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#rel_path = "../data/load/thrustcurve/AeroTech_D21.rse"
#rel_path = "../data/load/thrustcurve/AeroTech_H45.edx"
rel_path = "../data/load/thrustcurve/AeroTech_H45.txt"
abs_path = os.path.join(script_dir, rel_path)

file = open(abs_path, "r")
#print(file.read())

def converteng(file):
    #Returns list of lists
    pair = [0,0]
    curve = []
    for line in file:
        if line[0].isalpha():
            continue
        pair = [0,0]
        pair[0] = float(line.split()[0])
        pair[1] = float(line.split()[1])
        curve.append(pair)

    return curve

def convertrse(file):
    #returns list of lists
    pair = [0,0]
    curve = []
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root[0][0][1]:
        pair = [0,0]
        pair[0] = float(child.attrib["t"])
        pair[1] = float(child.attrib["f"])
        curve.append(pair)
    return curve

def convertedx(file):
    #return list of lists
    pair = [0,0]
    curve = []
    linenum = 0
    for line in file:
        pair = [0,0]
        if int(line.split()[0]) != 20: #checks that we're inside the thrust curve
            continue
        pair[0] = float(line.split("  ")[1].split()[2]) #splits on double space, then on single space
        pair[1] = float(line.rsplit(" ", 1)[1].rstrip("\r\n")) #splits from right once, removes newline character
        curve.append(pair)
        ++linenum
    return curve

def convertcompuroc(file):
    #return list of lists
    pair = [0,0]
    curve = []
    for line in file:
        pair = [0,0]
        if line[0].isalpha() or line[0] == ";" or line[0] == "-":
            continue
        pair[0] = float(line.split()[0])
        pair[1] = float(line.split()[1])
        curve.append(pair)

    return curve

print(convertcompuroc(file))
