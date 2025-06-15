from pymatgen.io.vasp import Poscar
from pymatgen.core.surface import SlabGenerator
import numpy as np

# Load the initial POSCAR
structure = Poscar.from_file(r'E:\Onedrive\Calculations\NH3\cracking\bulk\PBE\CoNi_MPRelaxSet\CONTCAR').structure

# Generate (1, 1, 1) slab with 6 layers and 20 Å vacuum
miller_index = (1, 1, 1)
slabgen = SlabGenerator(structure, miller_index, min_slab_size=6, min_vacuum_size=13, center_slab=True,
                        in_unit_planes=True, max_normal_search=1)

slabs = slabgen.get_slabs()
print(len(slabs))
slab = slabs[0]

# Create a 3x3 supercell in x-y
supercell_structure = slab.copy()
supercell_structure.make_supercell([3, 3, 1])

# Identify bottom three layers to fix
coords = supercell_structure.frac_coords
z_coords = coords[:, 2]
unique_z = np.unique(np.sort(z_coords))
bottom_layers = unique_z[:len(unique_z)//2]

# Apply selective dynamics to fix bottom layers
selective_dynamics = []
for coord in coords:
    if coord[2] in bottom_layers:
        selective_dynamics.append([False, False, False])
    else:
        selective_dynamics.append([True, True, True])

supercell_structure.add_site_property("selective_dynamics", selective_dynamics)
# # Adjust selective dynamics for supercell
# selective_dynamics_supercell = selective_dynamics * 9  # replicating for supercell
# supercell_structure.add_site_property("selective_dynamics", selective_dynamics_supercell)

# Write supercell POSCAR
supercell_poscar = Poscar(supercell_structure, selective_dynamics=selective_dynamics, sort_structure=True)
supercell_poscar.write_file(r'E:\Onedrive\Calculations\NH3\cracking\bulk\PBE\CoNi_MPRelaxSet\CoMo.poscar.111.vasp')
