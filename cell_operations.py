from ase.io import read, write
import numpy as np


def orthogonalize_cell(ase_atoms):
    """
    Convert a tilted cell into an orthogonal one while perserving its original volume
    :param ase_atoms: ASE atoms object
    :return:
    """
    cell_matrix = ase_atoms.get_cell()
    u, s, vh = np.linalg.svd(cell_matrix.array.astype(np.float64), full_matrices=True)
    current_vol = np.abs(np.linalg.det(cell_matrix.array))
    transformation = np.linalg.solve(cell_matrix.array, s * np.identity(3))
    new_cell = np.matmul(cell_matrix.array, transformation)
    new_cell_vol = np.abs(np.linalg.det(new_cell))
    assert np.allclose(current_vol, new_cell_vol), "Volume is not preserved after transformation!"
    positions = ase_atoms.get_positions()
    new_positions = np.matmul(positions, transformation)
    atoms.set_cell(new_cell, scale_atoms=True)
    print(np.subtract(new_positions, ase_atoms.get_positions()))
    assert np.allclose(ase_atoms.get_positions(), new_positions), "inconsistency between atom positions calculated " \
                                                                  "manually and with ASE scale_atoms!"


if __name__ == "__main__":
    path_ = r"E:\calc_results\PTC\TOL_H2O_GAMMA_ONLY\ML_ITER9\vasprun.xml"
    atoms = read(path_, index=-1)
    orthogonalize_cell(atoms)
    write(r"E:\calc_results\PTC\TOL_H2O_GAMMA_ONLY\POSCAR", images=atoms)
