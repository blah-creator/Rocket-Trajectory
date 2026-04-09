import numpy as np

burn_time = 2.09

thrust_time = np.array([0.0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.09])
thrust_values = np.array([0.0, 10.0, 15.0, 16.0, 18.0, 16.0, 10.0, 0.0])


def get_thrust(t):
    if t > burn_time:
        return 0.0
    return np.interp(t, thrust_time, thrust_values)


dt = 0.01
t = 0
while t < burn_time:
    print(get_thrust(t))
    t += dt
