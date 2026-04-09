from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.lines import Line2D

burn_time = 2.09
ejection_delay = 8.0


def plot_3d_trajectory(height, x_position, y_position, time):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    phase = []
    for t in time:
        if t <= burn_time:
            phase.append(0)
        elif t <= burn_time + ejection_delay:
            phase.append(1)
        else:
            phase.append(2)
    phase = np.array(phase)
    cmap = ListedColormap(["red", "blue", "green"])
    points = np.array([x_position, y_position, height]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = Normalize(vmin=0, vmax=2)
    lc = Line3DCollection(segments, cmap=cmap, norm=norm, linewidth=2)
    lc.set_array(phase[:-1])

    ax.add_collection(lc)

    ax.set_xlabel("X Position(N-S)(m)")
    ax.set_ylabel("Y Position(E-W)(m)")
    ax.set_zlabel("Altitude(m)")
    ax.set_title("3D Rocket Trajectory")

    ax.plot(x_position, y_position, [0] * len(x_position), color="gray", alpha=0.3)

    legend = [
        Line2D([0], [0], color="red", lw=2, label="Burn"),
        Line2D([0], [0], color="blue", lw=2, label="Coast"),
        Line2D([0], [0], color="green", lw=2, label="Parachute"),
    ]

    ax.legend(handles=legend)

    ax.set_xlim(min(x_position), max(x_position))
    ax.set_ylim(min(y_position), max(y_position))
    ax.set_zlim(0, max(height))

    plt.show()
