from rocket_sim import module_rocket as mr
import numpy as np

dt = 1
ang_velocity = np.array([1, 0, 0])
ang_delta = np.array([0, 0, 0])

ang_delta = ang_velocity * dt

print(mr.rodrigues(ang_delta))
