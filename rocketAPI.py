import numpy as np
from small_functions import (
    drag_force,
    drag_fin,
    base_drag,
    acceleration,
    get_thrust,
    get_mass,
    get_parachute_drag,
    get_3d_drag,
    get_wind,
    get_directional_thrust,
)

""""
app = FastAPI()
"""
g = 9.81
burn_time = 2.09


def simulate_flight(rocket, dry_rocket_mass, tip_chord, root_chord, fin_height):
    dt = 0.01
    t = 0
    h = 0
    x_pos = 0
    y_pos = 0
    time = []
    vel = []
    altitude = []
    accel = []
    thrust_curve = []
    mass_list = []
    x_position = []
    y_position = []
    max_h = 0
    ejection_delay = 8.0
    vx = 0
    vz = 0
    vy = 0

    while h >= 0 or vz > 0:
        if t > burn_time:
            T = 0
            T_x = 0
            T_y = 0
            T_z = 0
        else:
            T = get_thrust(t)
            thrust_dir = get_directional_thrust(vx, vy, vz)
            T_x = T * thrust_dir[0]
            T_y = T * thrust_dir[1]
            T_z = T * thrust_dir[2]

        mass = get_mass(t) + dry_rocket_mass
        mass_list.append(mass)

        wind_speed_x, wind_speed_y = get_wind(h)

        v_rel_x = vx - wind_speed_x
        v_rel_y = vy - wind_speed_y
        v_rel_z = vz
        v_rel = np.sqrt(v_rel_x**2 + v_rel_y**2 + v_rel_z**2)

        if t >= burn_time + ejection_delay:
            d_parachute = get_parachute_drag(v_rel, h)
            drag_f = drag_force(rocket.diameter, v_rel, h)
            base_D = base_drag(v_rel, rocket.diameter, h)
            fin_drag = drag_fin(tip_chord, root_chord, fin_height, v_rel, h)
            total_drag = drag_f + d_parachute + base_D + fin_drag
        else:
            drag_f = drag_force(rocket.diameter, v_rel, h)
            base_D = base_drag(v_rel, rocket.diameter, h)
            fin_drag = drag_fin(tip_chord, root_chord, fin_height, v_rel, h)
            total_drag = base_D + drag_f + fin_drag
        D_x, D_z, D_y = get_3d_drag(v_rel, v_rel_x, v_rel_z, total_drag, v_rel_y)
        az, ax, ay = acceleration(mass, D_y, D_x, D_z, T_x, T_y, T_z)

        vz += az * dt
        vx += ax * dt
        vy += ay * dt
        h += vz * dt
        x_pos += vx * dt
        y_pos += vy * dt
        t += dt
        x_position.append(x_pos)
        y_position.append(y_pos)
        vel.append(vz)
        time.append(t)
        altitude.append(h)
        accel.append(ay)
        thrust_curve.append(T)

        if h > max_h:
            max_h = h

    return (
        max_h,
        time,
        altitude,
        vel,
        accel,
        thrust_curve,
        mass_list,
        x_position,
        y_position,
    )


""""
@app.get("/trajectory")
def trajectory(burn_time: float, thrust: float, mass: float):
    max_height, time, altitude, velocity, acceleration = simulate_flight(
        burn_time, thrust, mass
    )
    return {
        "max_height": max_height,
        "altitude": altitude,
        "time": time,
        "velocity": velocity,
        "acceleration": acceleration,
    }
"""
