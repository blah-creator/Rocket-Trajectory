from small_functions import (
    nc_area,
    fin_area,
    engine_mount_area,
    body_area_not_engine,
    cross_area,
)

p_material = 1050
inch_to_m = 0.0254
m_to_inch = 39.3701
m_to_feet = 3.28084
fin_thickness = 0.002
engine_mass = 0.0828
engine_length = 2.95 * inch_to_m
engine_width = 1.149 * inch_to_m
edge_thick = 0.2 * inch_to_m


def calculate_cg(rocket):
    nose_mass = p_material * nc_area(rocket)
    fin_mass = p_material * fin_area(rocket)
    engine_mount_mass = p_material * engine_mount_area(rocket)
    body_mass = p_material * body_area_not_engine(rocket)
    total_mass = nose_mass + fin_mass + engine_mount_mass + body_mass + engine_mass

    nose_pos = rocket.nc_length / 2
    body_pos = rocket.nc_length + (rocket.length - engine_length) / 2
    fin_pos = rocket.length - (rocket.fin_height / 2)
    engine_pos = rocket.length - (engine_length / 2)
    engine_mount_pos = rocket.length - (engine_length / 2)

    x_cg = (
        nose_mass * nose_pos
        + body_mass * body_pos
        + fin_mass * fin_pos
        + engine_mass * engine_pos
        + engine_mount_mass * engine_mount_pos
    ) / total_mass

    return x_cg


def calculate_cp(rocket):
    n_fins = 3
    body_cross_area = cross_area(rocket.diameter)
    a_fin = n_fins * (((rocket.tip_chord + rocket.root_chord) / 2) * rocket.fin_height)
    cn_nose = 2
    cn_fin = a_fin / body_cross_area
    x_nose = (2 / 3) * rocket.nc_length
    x_fins = rocket.length - (rocket.root_chord / 3)
    x_cp = ((cn_nose * x_nose) + (cn_fin * x_fins)) / (cn_fin + cn_nose)
    return x_cp


def stability_margin(x_cg, x_cp, rocket):
    sta_margin = (x_cp - x_cg) / rocket.diameter
    return sta_margin
