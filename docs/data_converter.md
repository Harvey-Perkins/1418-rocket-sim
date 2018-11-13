This set of modules loads data from /data/thrustcurve/* and converts it into lists, then into cubic spline functions.
main.thrustcurve(rel_path)
rel_path should be a string that is a file path of the format "../data/load/thrustcurve/[file name here]"
It will interpolate the data and return a function that will produce pretty good "in-between" values for all the time that the engine has data.
Make sure that any place that uses that function checks that the values passed into it aren't above or below the data range.
