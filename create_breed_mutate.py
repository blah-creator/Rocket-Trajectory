from rocketclass import Rocket
import random

inch_to_m = 0.0254
m_to_inch = 39.3701
m_to_feet = 3.28084
fin_thickness = 0.002
engine_mass = 0.0828
engine_length = 2.95 * inch_to_m
engine_width = 1.149 * inch_to_m
edge_thick = 0.2 * inch_to_m


def breed(parent1, parent2):
    return Rocket(
        length=random.choice([parent1.length, parent2.length]),
        diameter=random.choice([parent1.diameter, parent2.diameter]),
        fin_height=random.choice([parent1.fin_height, parent2.fin_height]),
        root_chord=random.choice([parent1.root_chord, parent2.root_chord]),
        tip_chord=random.choice([parent1.tip_chord, parent2.tip_chord]),
        nc_length=random.choice([parent1.nc_length, parent2.nc_length]),
    )


def mutate(rocket):
    rocket.length += random.uniform(-2, 2) * inch_to_m
    if rocket.length < 15:
        rocket.length = 15
    rocket.diameter += random.uniform(-0.5, 0.5) * inch_to_m
    if rocket.diameter < 1.35:
        rocket.diameter = 1.35
    rocket.fin_height += random.uniform(-0.2, 0.2) * inch_to_m
    if rocket.fin_height <= 0.5:
        rocket.fin_height = 0.5
    elif rocket.fin_height >= 3:
        rocket.fin_height = 3
    rocket.root_chord += random.uniform(-0.2, 0.2) * inch_to_m
    if rocket.root_chord <= 0.5:
        rocket.root_chord = 0.5
    elif rocket.root_chord >= 3:
        rocket.root_chord = 3
    rocket.tip_chord += random.uniform(-0.1, 0.1) * inch_to_m
    if rocket.tip_chord <= 0.5:
        rocket.tip_chord = 0.5
    elif rocket.tip_chord >= 2:
        rocket.tip_chord = 2
    rocket.nc_length += random.uniform(-0.25, 0.25) * inch_to_m
    if rocket.nc_length <= 2.5:
        rocket.nc_length = 2.5
    elif rocket.nc_length >= 6:
        rocket.nc_length = 6

    return rocket


def create_random_rocket():

    return Rocket(
        length=random.uniform(15, 30) * inch_to_m,
        diameter=random.uniform(1.4, 2.5) * inch_to_m,
        fin_height=random.uniform(1, 3) * inch_to_m,
        root_chord=random.uniform(1, 3) * inch_to_m,
        tip_chord=random.uniform(0.5, 2) * inch_to_m,
        nc_length=random.uniform(2, 6) * inch_to_m,
    )
