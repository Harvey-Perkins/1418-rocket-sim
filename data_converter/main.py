import convert
import os

'''Eventually, this will run all the modules''''

script_dir = os.path.dirname(__file__)
rel_path = "../data/load/thrustcurve/"
abs_path = os.path.join(script_dir, rel_path) #connects the path of where the file is being run, __file__, with the relative path of the data

for filename in os.listdir(abs_path):
    file = open(os.path.join(abs_path, filename), "r")
    print(file.name.rsplit("/",1)[1]) #debug
    if file.name.rsplit("/", 1)[1] == "00INDEX.txt": #Ignores index
        continue
    elif file.name.rsplit(".", 1)[1] == "eng": #detects file extension
        print(convert.converteng(file))
    elif file.name.rsplit(".", 1)[1] == "rse":
        print(convert.convertrse(file))
    elif file.name.rsplit(".", 1)[1] == "edx":
        print(convert.convertedx(file))
    elif file.name.rsplit(".", 1)[1] == "txt":
        print(convert.convertcompuroc(file))
