from ase.io import read
from ase.units import kg, m, _amu
import numpy as np
import pandas as pd


def print_densities(ase_atoms):
    """
    Calculate and return density in kg/m3
    :param ase_atoms:
    :type ase_atoms: ase.Atoms
    :return:
    """
    cell_matrix = ase_atoms.get_cell()
    current_vol = np.abs(np.linalg.det(cell_matrix.array))
    atoms_masses = ase_atoms.get_masses()
    density = np.sum(atoms_masses)/current_vol * (_amu/1e-30)
    return density


if __name__ == "__main__":
    path_ = r"E:\calc_results\PTC\TOLUENES_GAMMA_ONLLY\orthogonal\ML_ITER3\XDATCAR"
    ensemble = read(path_, index=":")
    all_densities = [print_densities(atoms) for atoms in ensemble]
    df = pd.Series(all_densities)
    print(df.describe())


