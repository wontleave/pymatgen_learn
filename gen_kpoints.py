import numpy as np
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.io.vasp import Poscar, Kpoints
from atomate.vasp.workflows.base.adsorption import get_wf_slab
from ase.io.vasp import write_vasp
from ase.io import read
from os import path
from pathlib import Path

if __name__ == "__main__":
    full_path = r"E:\calc_results\NiPt MPRelaxSet\PBE-D3BJ\OPT_ISIF8\Pt_FCC\111\0\POSCAR"
    structure = Structure.from_file(full_path)
    kpoints = Kpoints.automatic_density_by_vol(structure, 200)
    # kpoints = Kpoints.automatic_gamma_density(structure, 0.2)

    full_path = path.join(path.dirname(full_path), "KPOINTS")
    print(f"Writing to {full_path}")
    kpoints.write_file(full_path)