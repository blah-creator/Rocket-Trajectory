from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def plot_3d_trajectory(height, x_position, y_position):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(x_position, y_position, height, color="blue", linewidth=2)

    ax.set_xlabel("X Position(N-S)(m)")
    ax.set_ylabel("Y Position(E-W)(m)")
    ax.set_zlabel("Altitude(m)")
    ax.set_title("3D Rocket Trajectory")

    ax.plot(x_position, y_position, [0] * len(x_position), color="gray", alpha=0.3)

    plt.show()
