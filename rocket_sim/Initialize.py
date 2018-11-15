"""
This should start the actual program, importing modules and classes, as well as starting any GUIs.
It should either initialize all the variables and contain the main loop, or directly call a module that does.
"""

import module_engine as me

#file_path = "../data/load/thrustcurve/AeroTech_D10.eng"
#file_path = "../data/load/thrustcurve/AeroTech_D21.rse"
#file_path = "../data/load/thrustcurve/AeroTech_H45.edx"
file_path = "../data/load/thrustcurve/AeroTech_H125.txt"

engine1 = me.Engine(file_path)

print(engine1.curve)

#Testing class stuff
