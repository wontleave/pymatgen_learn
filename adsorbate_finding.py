from pymatgen.core import Structure, Molecule
from pymatgen.analysis.adsorption import *
from os import path
from pathlib import Path
from pymatgen.io.vasp import Poscar

if __name__ == "__main__":
    full_path = r"E:\calc_results\Electrochem\Mo-Co\1Mo8Co\ML_ISIF3\CONTCAR"
    structure = Structure.from_file(full_path)
    asf_moco = AdsorbateSiteFinder(structure)
    ads_sites = asf_moco.find_adsorption_sites()
    for key in ads_sites.keys():
        print(key)
        print(ads_sites[key])

    # Change Adsorbate here
    ads = Molecule("OH", [[0, 0, 0], [0, 0.96, 0]])
    ads_structs = asf_moco.generate_adsorption_structures(ads)

    new_root = path.join(path.dirname(full_path), f"OH_ads")

    for n, structs in enumerate(ads_structs):
        where = path.join(new_root, f"{n}")
        Path(where).mkdir(parents=True, exist_ok=True)
        full_path = path.join(where, "POSCAR")
        Poscar(structs, comment="MoCoO2_O2ads", sort_structure=True).write_file(full_path)
