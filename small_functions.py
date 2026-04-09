import numpy as np

g = 9.81
# thrust = 16
burn_time = 2.09
p_material = 1050
cd_fin = 0.04
inch_to_m = 0.0254
m_to_inch = 39.3701
m_to_feet = 3.28084
fin_thickness = 0.002
engine_mass = 0.0828
engine_length = 2.95 * inch_to_m
engine_width = 1.149 * inch_to_m
edge_thick = 0.2 * inch_to_m
speed_of_sound = 343
dry_mass = 0.0435
fuel_mass = 0.04
initial_mass = dry_mass + fuel_mass
parachute_cd = 1.5
parachute_diameter = 0.3
parachute_area = np.pi * (parachute_diameter / 2) ** 2

thrust_time = np.array([0.0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.09])
thrust_values = np.array([4.5, 10.0, 15.0, 16.0, 18.0, 16.0, 10.0, 0.0])


def get_thrust(t):
    # if t > burn_time:
    # return 0.0
    return np.interp(t, thrust_time, thrust_values)


def get_mass(t):
    if t > burn_time:
        mass = dry_mass
        return mass
    fuel_left = fuel_mass * (1 - t / burn_time)
    mass = fuel_left + dry_mass
    return mass


def get_cd(velocity):
    mach = abs(velocity) / speed_of_sound
    if mach < 0.8:
        cd = 0.4
    elif 0.8 <= mach <= 1.2:
        cd = 0.4 + (mach - 0.8) * 1.5
    else:
        cd = 0.7
    return cd


def get_rho(h):
    rho_h = 1.225 * np.exp((-h) / 8500)
    return rho_h


def get_parachute_drag(v_rel, h):
    rho = get_rho(h)
    D = 0.5 * rho * parachute_cd * parachute_area * v_rel * abs(v_rel)
    return D


def base_drag(v_rel, diameter, h):
    cd = 0.12
    rho = get_rho(h)
    area = cross_area(diameter)
    base_D = 0.5 * rho * area * cd * v_rel * abs(v_rel)
    return base_D


def cross_area(diameter):
    r = diameter / 2
    area = np.pi * (r**2)
    return area


def fin_area(rocket):
    fin_a = 3 * (
        ((rocket.tip_chord + rocket.root_chord) / 2) * rocket.fin_height * fin_thickness
    )
    return fin_a


def engine_mount_area(rocket):
    engine_mount_a = ((((rocket.diameter / 2) ** 2) * np.pi) * engine_length) - (
        ((engine_width / 2) ** 2) * np.pi
    ) * engine_length
    return engine_mount_a


def body_area_not_engine(rocket):
    body_area = (
        (rocket.diameter / 2) ** 2 * np.pi * (rocket.length - engine_length)
    ) - (
        ((rocket.diameter - edge_thick) / 2) ** 2
        * np.pi
        * (rocket.length - engine_length)
    )
    return body_area


def nc_area(rocket):
    nc_a = (1 / 3) * (rocket.diameter / 2) ** 2 * np.pi * rocket.nc_length
    return nc_a


def drag_force(diameter, v_rel, h):
    cd = get_cd(v_rel)
    rho = get_rho(h)
    D = rho * cd * cross_area(diameter) * (v_rel * abs(v_rel)) * 0.5
    return D


def drag_fin(tip_chord, root_chord, fin_height, v_rel, h):
    rho = get_rho(h)
    D_fin = 3 * (
        rho
        * cd_fin
        * (v_rel * abs(v_rel))
        * 0.5
        * (((tip_chord + root_chord) / 2) * fin_height)
    )
    return D_fin


def acceleration(mass, D_y, D_x, T, D_z):
    az = (T - D_z - (mass * g)) / mass
    ax = -D_x / mass
    ay = -D_y / mass
    return az, ax, ay


def get_3d_drag(v_rel, v_rel_x, v_rel_z, D_total, v_rel_y):
    if v_rel == 0:
        D_x, D_y = 0, 0
    else:
        D_x = D_total * (
            v_rel_x / v_rel
        )  # Assuming drag is proportional to velocity components
        D_y = D_total * (
            v_rel_y / v_rel
        )  # Assuming drag is proportional to velocity components
        D_z = D_total * (v_rel_z / v_rel)
    return D_x, D_z, D_y
