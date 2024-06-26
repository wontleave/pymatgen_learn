from pymatgen.io.xyz import XYZ
from os import path
from pymatgen.io.vasp import Poscar


if __name__ == "__main__":

    xyz_name = r"E:\calc_results\PtNi_nanowire\Adsorbate\MeOH\meoh.xyz"
    mol = XYZ.from_file(xyz_name)
    mol_in_box = mol.molecule.get_boxed_structure(30.0, 30.0, 30.0)
    out_name = path.join(path.dirname(xyz_name), f"POSCAR")
    Poscar(mol_in_box, comment="Methanol", sort_structure=True).write_file(out_name)