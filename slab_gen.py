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

full_filename = r"E:\calc_results\CaF2\CONTCAR"
phenol = read(r"E:\calc_results\CaF2\phenol.xyz")
pymategen_phenol = AseAtomsAdaptor.get_molecule(phenol)

ca_f2 = Structure.from_file(full_filename)
ca_f2.add_oxidation_state_by_element({"Ca": 2, "F": -1})
slabgen = SlabGenerator(ca_f2, miller_index=(2, 1, 0),
                        in_unit_planes=True,
                        min_slab_size=5, min_vacuum_size=10, center_slab=True, reorient_lattice=True)
slabs = slabgen.get_slabs()

ca_f2_path = Path(full_filename)
from atomate.vasp.workflows.base.adsorption import MPSurfaceSet

for n, slab in enumerate(slabs):
    # slab.make_supercell([2, 2, 1])
    # wf = get_wf_slab(slab, adsorbates=[pymategen_phenol])
    new_root = path.join(ca_f2_path.parent, "210")
    ads = AdsorbateSiteFinder(slab, selective_dynamics=True, height=2.5).\
        generate_adsorption_structures(pymategen_phenol, repeat=(2, 2, 1), find_args={"distance": 3.0})

    # for i, item in enumerate(wf):
    #     s = MPSurfaceSet(item.tasks[0]["structure"])
    #     where = path.join(new_root, str(i))
    #     Path(where).mkdir(parents=True, exist_ok=True)
    #     s.write_input(output_dir=where)

    for i, ad in enumerate(ads):
        where = path.join(new_root, str(i))
        Path(where).mkdir(parents=True, exist_ok=True)
        full_path = path.join(where, "POSCAR")
        Poscar(ad).write_file(full_path)
        # ase_slab = AseAtomsAdaptor.get_atoms(slab)
        # write_vasp(full_path, ase_slab)