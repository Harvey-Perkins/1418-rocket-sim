from data_converter import convert
import os
import matplotlib.pyplot as plt
import numpy as np
import bezier
from scipy.interpolate import CubicSpline

xs = []
ys = []
cubicx = []
cubicy = []

'''
Takes a file and creates pretty graphs of it with both cubic interpolation and bezier curve fitting.
'''
'''
script_dir = os.path.dirname(__file__)
#rel_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#rel_path = "../data/load/thrustcurve/AeroTech_D21.rse"
rel_path = "../data/load/thrustcurve/AeroTech_H45.edx"
#rel_path = "../data/load/thrustcurve/AeroTech_H125.txt"
abs_path = os.path.join(script_dir, rel_path) #connects the path of where the file is being run, __file__, with the relative path of the data
file = open(abs_path)

#data = convert.converteng(file) #test
#data = convert.convertrse(file) #test
data = convert.convertedx(file) #test
#data = convert.convertcompuroc(file) #This is the only one that doesn't work with bezier

#converts from list of x y pairs to list of x and list of y coords
'''

def cubiccurve(data):
    #takes output of convert.py
    xs = []
    ys = []

    for pair in data:
        xs.append(pair[0])
        ys.append(pair[1])

    #graphs the raw data
    #plt.plot(xs, ys)
    #plt.show()

    cubic = CubicSpline(xs, ys, bc_type="natural")
    return cubic

def beziercurve(data):
    xs = []
    ys = []
    #Takes ouput from convert.py
    for pair in data:
        xs.append(pair[0])
        ys.append(pair[1])

    nodes = np.asfortranarray([xs,ys])

    curve1 = bezier.Curve.from_nodes(nodes)
    return curve1

#cubiccurve(data)
'''
#Cubic Spline graph
for i in range(256):
    cubicx.append(i * xs[len(xs) - 1]/256)
    cubicy.append(cubic(i * xs[len(xs) - 1]/256)) #this horrible mess creates 256 points within the range of the original

plt.plot(cubicx, cubicy)
plt.show()


#Bezier graph
#curve1.plot(num_pts=256)
#plt.show()
'''
