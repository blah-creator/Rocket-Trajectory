from small_functions import (
    drag_force,
    drag_fin,
    base_drag,
    acceleration,
    get_thrust,
    get_mass,
    get_parachute_drag,
)

""""
app = FastAPI()
"""
g = 9.81
burn_time = 2.09


def simulate_flight(rocket, dry_rocket_mass, tip_chord, root_chord, fin_height):
    dt = 0.01
    velocity = 0
    t = 0
    h = 0
    time = []
    vel = []
    altitude = []
    accel = []
    thrust_curve = []
    mass_list = []
    max_h = 0
    ejection_delay = 6.0

    while h >= 0 or velocity > 0:
        if t > burn_time:
            T = 0
        else:
            T = get_thrust(t)
            # T = 16

        mass = get_mass(t) + dry_rocket_mass
        mass_list.append(mass)

        if t >= burn_time + ejection_delay:
            d_parachute = get_parachute_drag(velocity, h)
            drag_f = drag_force(rocket.diameter, velocity, h)
            base_D = base_drag(velocity, rocket.diameter, h)
            fin_drag = drag_fin(tip_chord, root_chord, fin_height, velocity, h)
            total_drag = drag_f + d_parachute + base_D + fin_drag
        else:
            drag_f = drag_force(rocket.diameter, velocity, h)
            base_D = base_drag(velocity, rocket.diameter, h)
            fin_drag = drag_fin(tip_chord, root_chord, fin_height, velocity, h)
            total_drag = base_D + drag_f + fin_drag
        a = acceleration(mass, total_drag, T)

        velocity += a * dt
        h += velocity * dt
        t += dt
        vel.append(velocity)
        time.append(t)
        altitude.append(h)
        accel.append(a)
        thrust_curve.append(T)

        if h > max_h:
            max_h = h

    return max_h, time, altitude, vel, accel, thrust_curve, mass_list


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
