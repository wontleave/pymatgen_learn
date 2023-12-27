import numpy as np
from pymatgen.core.structure import Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.io.vasp import Poscar
from atomate.vasp.workflows.base.adsorption import get_wf_slab
from ase.io.vasp import write_vasp
from ase.io import read
from os import path
from pathlib import Path

if __name__ == "__main__":
    full_path = r"E:\Downloads\NiPt.cif"
    m1 = 1
    m2 = 1
    m3 = 1
    input_struct = Structure.from_file(full_path)
    input_struct.add_oxidation_state_by_element({"Ni": 2, "Pt": -2, "H": 0})
    slabgen = SlabGenerator(input_struct, miller_index=(m1, m2, m3),
                            in_unit_planes=True,
                            min_slab_size=3, min_vacuum_size=10, center_slab=True, reorient_lattice=True,
                            max_normal_search=-10)
    slabs = slabgen.get_slabs()
    new_root = path.join(path.dirname(full_path), f"{m1}{m2}{m3}")

    for n, slab in enumerate(slabs):
        slab.make_supercell([3, 3, 1])
        where = path.join(new_root, str(n))
        Path(where).mkdir(parents=True, exist_ok=True)
        full_path = path.join(where, "POSCAR")
        print(f"Writing to {full_path}")
        Poscar(slab).write_file(full_path)
