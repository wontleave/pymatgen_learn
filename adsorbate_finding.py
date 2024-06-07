from pymatgen.core import Structure, Molecule
from pymatgen.transformations.standard_transformations import RotationTransformation
from pymatgen.analysis.adsorption import *
from os import path
from pathlib import Path
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    full_path = r"E:\calc_results\PtNi_nanowire\Ni111_ortho\OPT\CONTCAR"
    structure = Structure.from_file(full_path)
    asf_moco = AdsorbateSiteFinder(structure)
    ads_sites = asf_moco.find_adsorption_sites()
    for key in ads_sites.keys():
        print(key)
        print(ads_sites[key])

    # Change Adsorbate here
    ads = Molecule("HHHCOH", [
        [1.35206053, 1.28652446, 0.87304626],
        [1.35205998, 1.28652441, -0.87425639],
        [2.05138451, -0.05539439, -0.00060489],
        [1.26887524, 0.67438588, -0.00060502],
        [0.00074629, 0.01351603, -0.00060502],
        [-0.70131752, 0.66827044, 0.00115002]
    ])
    rotate = RotationTransformation(axis=(1, 0, 0), angle=90)
    ads_structs = asf_moco.generate_adsorption_structures(rotate.apply_transformation(ads))

    new_root = path.join(path.dirname(full_path), f"MeOH_ads")

    for n, structs in enumerate(ads_structs):
        where = path.join(new_root, f"{n}")
        Path(where).mkdir(parents=True, exist_ok=True)
        full_path = path.join(where, "POSCAR")
        Poscar(structs, comment="CO_Pt111", sort_structure=True).write_file(full_path)
