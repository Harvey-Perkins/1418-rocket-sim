'''pulls the mass out of formats where it is available'''

import xml.etree.ElementTree as ET

def mass_eng(file):
    #Returns [wet mass, prop mass] in kg
    masses = []
    first_line = file.readline().split()
    masses.append(float(first_line[5]))
    masses.append(float(first_line[4]))
    return masses

def mass_rse(file):
    #Returns [wet mass, prop mass] in kg
    masses = []
    tree = ET.parse(file)
    root = tree.getroot()
    masses.append(float(root[0][0].attrib["initWt"])/1000)
    masses.append(float(root[0][0].attrib["propWt"])/1000)
    return masses
