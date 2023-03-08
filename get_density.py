from ase.io import read
from ase.units import kg, m, _amu, _Nav
import numpy as np
import pandas as pd
import argparse


def get_density_in_particles_per_angstrom3(input_density, solvent_mass):
    """

    :param input_density:
    :type input_density: str
    :type solvent_mass: List of str
    :return:
    """

    # units setting
    m3_to_a3 = m ** 3

    # Parsing
    density_value, density_mass_unit, density_vol_unit = input_density.split("_")
    density_value = float(density_value)
    solvent_mass_kg_particle = []

    for item in solvent_mass:
        value, mass_unit, particle_unit = item.split("_")
        value = float(value)
        if particle_unit.lower() == "mol":
            value /= _Nav

        if mass_unit.lower() == "g":
            value /= 1000.0

        solvent_mass_kg_particle.append(value)

    if density_mass_unit.lower() == "g":
        density_value = float(density_value) / 1000.0

    if density_vol_unit.lower() == "m3":
        density_value /= m3_to_a3  # Convert to angstrom^3

    solvent_mass_kg_particle_inv = 1.0 / np.array(solvent_mass_kg_particle)
    solvent_density_particle_per_angstrom3 = solvent_mass_kg_particle_inv * density_value

    print(solvent_density_particle_per_angstrom3)

    return solvent_density_particle_per_angstrom3


if __name__ == "__main__":
    factor = get_density_in_particles_per_angstrom3("997_kg_m3", ["18_g_mol"])
    cube_vol = 4/3 * np.pi * 10000.0 ** 3
    particle_in_shape = factor * cube_vol
    print (f"{particle_in_shape}")
    print(f"{kg:e}")