import matplotlib.pyplot as plt


def plot_flight(
    time, altitude, velocity, acceleration, thrust, mass, x_position, y_position
):
    mass_grams = [x * 1000 for x in mass]

    plt.figure(figsize=(10, 5))
    plt.plot(time, altitude, label="Altitude (m)")
    plt.plot(time, velocity, label="Velocity (m/s)")
    plt.plot(time, acceleration, label="Acceleration (m/s²)")
    plt.plot(time, thrust, label="Thrust (N)")
    plt.plot(time, mass_grams, label="Mass (g)")
    plt.plot(time, x_position, label="X Position(E - W)(m)")
    plt.plot(time, y_position, label="Y Position(N - S)(m)")
    plt.legend()
    plt.title("Rocket Trajectory")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.savefig("rocket_trajectory.png")
    plt.grid()
    plt.show()

    landing_x = x_position[-1]
    landing_y = y_position[-1]
    landing_time = time[-1]
    print(f"Landing Position: {landing_x} m(+N, -S), {landing_y} m(+E, -W)")
    print(f"Landing Time: {landing_time}")
