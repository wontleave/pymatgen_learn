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
    full_path = r"E:\calc_results\CO2_to_MeOH\ZnO\ZnO.cif"

    input_struct = Structure.from_file(full_path)
    input_struct.add_oxidation_state_by_element({"Zn": 2, "O": -2})
    slabgen = SlabGenerator(input_struct, miller_index=(1, 0, 1),
                            in_unit_planes=True,
                            min_slab_size=2.5, min_vacuum_size=7, center_slab=True, reorient_lattice=True)
    slabs = slabgen.get_slabs()
    new_root = path.join(path.dirname(full_path), "101")

    for n, slab in enumerate(slabs):
        slab.make_supercell([4, 4, 1])
        where = path.join(new_root, str(n))
        Path(where).mkdir(parents=True, exist_ok=True)
        full_path = path.join(where, "POSCAR")
        Poscar(slab).write_file(full_path)
