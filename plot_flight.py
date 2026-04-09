import matplotlib.pyplot as plt


def plot_flight(time, altitude, velocity, acceleration, thrust, mass):
    mass_grams = [x * 1000 for x in mass]

    plt.figure(figsize=(10, 5))
    plt.plot(time, altitude, label="Altitude (m)")
    plt.plot(time, velocity, label="Velocity (m/s)")
    plt.plot(time, acceleration, label="Acceleration (m/s²)")
    plt.plot(time, thrust, label="Thrust (N)")
    plt.plot(time, mass_grams, label="Mass (g)")
    plt.legend()
    plt.title("Rocket Trajectory")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.savefig("rocket_trajectory.png")
    plt.grid()
    plt.show()
