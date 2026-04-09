from rocketclass import Rocket
from create_breed_mutate import breed, mutate, create_random_rocket
import random
from small_functions import nc_area, fin_area, engine_mount_area, body_area_not_engine
from stability import calculate_cg, calculate_cp, stability_margin
from rocketAPI import simulate_flight
from plot_flight import plot_flight
import pandas as pd

g = 9.81
thrust = 16
burn_time = 2.09
p_material = 1050
cd_fin = 0.04
inch_to_m = 0.0254
m_to_inch = 39.3701
m_to_feet = 3.28084
fin_thickness = 0.002
# engine_mass = 0.0828
engine_length = 2.95 * inch_to_m
engine_width = 1.149 * inch_to_m
edge_thick = 0.2 * inch_to_m


def main():
    best_altitude = -1
    best_rocket = None

    population_size = 150

    population = []
    for i in range(population_size):
        rocket = Rocket(
            length=random.uniform(15, 30) * inch_to_m,
            diameter=random.uniform(1.4, 2) * inch_to_m,
            fin_height=random.uniform(1, 3) * inch_to_m,
            root_chord=random.uniform(1, 3) * inch_to_m,
            tip_chord=random.uniform(0.5, 2) * inch_to_m,
            nc_length=random.uniform(2, 6) * inch_to_m,
        )
        population.append(rocket)

    generations = 200

    for gen in range(generations):
        scores = []
        for rocket in population:
            dry_rocket_mass = p_material * (
                nc_area(rocket)
                + body_area_not_engine(rocket)
                + engine_mount_area(rocket)
                + fin_area(rocket)
            )

            altitude, time, height, vel, accel, thrust_curve, mass_list = (
                simulate_flight(
                    rocket,
                    dry_rocket_mass,
                    rocket.tip_chord,
                    rocket.root_chord,
                    rocket.fin_height,
                )
            )

            x_cg = calculate_cg(rocket)
            x_cp = calculate_cp(rocket)
            sta_margin = stability_margin(x_cg, x_cp, rocket)
            if 1.8 <= sta_margin <= 2.5:
                if altitude > best_altitude:
                    best_altitude = altitude
                    best_rocket = (
                        rocket,
                        dry_rocket_mass,
                        x_cg,
                        x_cp,
                        sta_margin,
                        time,
                        height,
                        vel,
                        accel,
                        thrust_curve,
                        mass_list,
                    )
                scores.append((altitude, rocket))

        scores.sort(key=lambda x: x[0], reverse=True)
        top = scores[:10]
        elite = top[0][1]

        new_population = [elite]

        while len(new_population) < population_size - 20:
            parent1 = random.choice(top)[1]
            parent2 = random.choice(top)[1]

            child = breed(parent1, parent2)
            child = mutate(child)

            new_population.append(child)
        while len(new_population) < population_size:
            new_population.append(create_random_rocket())

        population = new_population

        print("Generation", gen, "Best Altitude", scores[0][0] * m_to_feet)

    best_time = best_rocket[5]
    best_height = best_rocket[6]
    best_vel = best_rocket[7]
    best_accel = best_rocket[8]
    best_thrust = best_rocket[9]
    best_mass_list = best_rocket[10]
    plot_flight(
        best_time, best_height, best_vel, best_accel, best_thrust, best_mass_list
    )

    results = {
        "Best Altitude (feet)": best_altitude * m_to_feet,
        "Length (inches)": best_rocket[0].length * m_to_inch,
        "Diameter (inches)": best_rocket[0].diameter * m_to_inch,
        "Root Chord (inches)": best_rocket[0].root_chord * m_to_inch,
        "Tip Chord (inches)": best_rocket[0].tip_chord * m_to_inch,
        "Fin Height (inches)": best_rocket[0].fin_height * m_to_inch,
        "NC Length (inches)": best_rocket[0].nc_length * m_to_inch,
        "Mass (grams)": best_rocket[1] * 1000,
        "CG (inches)": best_rocket[2] * m_to_inch,
        "CP (inches)": best_rocket[3] * m_to_inch,
        "Stability Margin": best_rocket[4],
    }

    df = pd.DataFrame([results])
    df.to_csv("best_rocket.csv", index=False)


main()
