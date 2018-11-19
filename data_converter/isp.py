'''returns the exhaust velocity of engines when available'''

import xml.etree.ElementTree as ET

g0 = 9.81

def ve_rse(file):
    #Returns ve in m/s
    tree = ET.parse(file)
    root = tree.getroot()
    return float(root[0][0].attrib["Isp"]) * g0

def ve_edx(file):
    #returns ve in m/s
    lines =  file.readlines()
    for line in lines:
        if line.split()[0] == "62":
            return float(line.split()[3])*g0
