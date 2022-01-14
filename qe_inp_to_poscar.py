from pymatgen.io.pwscf import PWInput
from ase.io.espresso import read_espresso_in
from ase.io.vasp import write_vasp
import ase.build as ase_build
from ase.constraints import FixAtoms


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


full_path = r"E:\calc_results\ZXY\MP-674514\burai_slab_311\T1\pw.txt"
poscar_path = r"E:\calc_results\ZXY\MP-674514\burai_slab_311\T1\POSCAR"

# read a Quantum espresso input with ASE
with open(full_path, "r") as f:
    qe = read_espresso_in(f)

# get the indices of the atoms that are fixed
constraints_ = find_constraints(full_path)
fixed_atoms_idx = FixAtoms(constraints_)
qe.set_constraint(fixed_atoms_idx)
qe_sorted = ase_build.sort(qe)
qe.center(axis=2, about=0.)
# Write the VASP POSCAR
write_vasp(poscar_path, qe_sorted)
