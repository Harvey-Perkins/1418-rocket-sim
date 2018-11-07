'''
This isn't permenant, just a demo of the velocity verlet and how it can calculate velocity and position from a acceleration vector.
In this case, it just simulates dropping an object from a certain height.
'''

import numpy as np
g0 = np.array([0.0,0.0,-9.81])
position = np.array([0.0,0.0,10.0]) #does it matter if these are arrays vs. lists?
velocity = np.array([0.0,0.0,0.0])
t = 0
dt = 0.001

while position[2] > 0:
  t += dt
  position += velocity * dt + 0.5 * g0 *dt * dt #Just stealing this from someone else's implementation of the velocity verlet...
  velocity += g0 * dt

print(t)
