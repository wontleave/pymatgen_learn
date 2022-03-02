from pymatgen.io.pwscf import PWInput
from ase.io.espresso import read_espresso_in
from ase.io.vasp import write_vasp
import ase.build as ase_build
from ase.constraints import FixAtoms
import numpy as np
from os import path


def find_constraints(_file_path):
    """
    :param _file_path: self-explanatory
    :return: the indices of the atoms that have 0 0 0 in the QE input
    """
    with open(_file_path) as f:
        lines = f.readlines()

    constraint_idx = []
    read_coords = False
    for idx, line in enumerate(lines):
        if read_coords:
            temp = line.split()
            if len(temp) == 7:
                if temp[-1] == "0" and temp[-2] == "0" and temp[-3] == "0":
                    constraint_idx.append(idx)

        if "ATOMIC_POSITIONS {angstrom}" in line:
            read_coords = True

    return constraint_idx


def find_constraints_from_cartcoords(ase_obj, x=None, y=None, z=None):
    """
    Freeze atoms with cartesian coordinates that is less than or equal to the provided values
    :param constraints:
    :return:
    """
    coordinates = ase_obj.get_positions()
    z_only = coordinates[:, 2]
    req_idx = np.nonzero(z_only <= z)[0]
    return req_idx


root_path = r"E:\TEST\KOPh\plusTBAB"

full_path = path.join(root_path, "pw.txt")
poscar_path = path.join(root_path, "POSCAR")

# read a Quantum espresso input with ASE
with open(full_path, "r") as f:
    qe = read_espresso_in(f)

# ---------- get the indices of the atoms that are fixed from QE input
# constraints_ = find_constraints(full_path)
# fixed_atoms_idx = FixAtoms(constraints_)
# qe.set_constraint(fixed_atoms_idx)

# ---------- determine the atoms to freeze based on cartesian coordinates
fixed_atoms_idx = find_constraints_from_cartcoords(qe, z=6.97)
fixed_atoms_idx = FixAtoms(fixed_atoms_idx)

# ---------- Set the constraint if necessary
qe.set_constraint(fixed_atoms_idx)
qe_sorted = ase_build.sort(qe)
qe.center(axis=2, about=0.)
# Write the VASP POSCAR
write_vasp(poscar_path, qe_sorted)
