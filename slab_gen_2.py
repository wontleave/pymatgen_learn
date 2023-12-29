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


def unique_with_tolerance(arr, tol):
    # Sort the array
    sorted_arr = np.sort(arr)
    unique_vals = [sorted_arr[0]]

    for value in sorted_arr[1:]:
        # Check if the current value is within the tolerance of the last unique value
        if np.abs(value - unique_vals[-1]) > tol:
            unique_vals.append(value)

    return np.array(unique_vals)


# Find indices with tolerance
def find_indices_with_tolerance(array, unique_vals, tol):
    indices = []
    for i, value in enumerate(array):
        if any(np.abs(value - unique_val) <= tol for unique_val in unique_vals):
            indices.append(i)
    return np.array(indices)


if __name__ == "__main__":
    full_path = r"E:\calc_results\NiPt MPRelaxSet\PBE-D3BJ\OPT\tetragonalNiPt\POSCAR"
    m1 = 1
    m2 = 1
    m3 = 1
    input_struct = Structure.from_file(full_path)
    input_struct.add_oxidation_state_by_element({"Ni": 0, "Pt": -2})
    slabgen = SlabGenerator(input_struct, miller_index=(m1, m2, m3),
                            in_unit_planes=False,
                            min_slab_size=4, min_vacuum_size=15, center_slab=False, reorient_lattice=True, )
    # max_normal_search=-10)
    # vacuum layer will be scaled by the distance between unit planes in the OUC if in_unit_planes=True : complicates
    # min vacuum size.

    slabs = slabgen.get_slabs()
    new_root = path.join(path.dirname(full_path), f"{m1}{m2}{m3}")

    for n, slab in enumerate(slabs):
        slab.make_supercell([2, 2, 1])
        third_column = slab.frac_coords[:, 2]
        z_coords = unique_with_tolerance(third_column, 1e-6)
        indices = find_indices_with_tolerance(third_column, z_coords[:len(z_coords) // 2], 1e-6)
        # Create an array of the shape as frac_coords
        bool_array = np.zeros(slab.frac_coords.shape, dtype=bool)
        all_indices = np.arange(slab.frac_coords.shape[0])
        not_in_indices = np.in1d(all_indices, indices, invert=True)
        bool_array[not_in_indices, :] = True

        where = path.join(new_root, str(n))
        Path(where).mkdir(parents=True, exist_ok=True)
        full_path = path.join(where, "POSCAR")
        print(f"Writing to {full_path}")
        Poscar(slab, sort_structure=True, selective_dynamics=bool_array).write_file(full_path)
