from pymatgen.io.vasp import Vasprun
from pymatgen.io.vasp.outputs import Eigenval, BSVasprun
from pymatgen.electronic_structure.plotter import DosPlotter
from os import path

root_path = r"E:\calc_results\ZXY\MP-674514\burai_slab_311\T1\HSE06-u0p13"
xml_path = path.join(root_path, "vasprun.xml")
eigen_path = path.join(root_path, "EIGENVAL")


eigen = Eigenval(eigen_path)
print(eigen.eigenvalue_band_properties)

# vasp_run = Vasprun(xml_path)
# cdos = vasp_run.complete_dos
# element_dos = cdos.get_element_dos()
# plotter = DosPlotter(sigma=0.01)
# plotter.add_dos_dict(element_dos)
# plotter.show(xlim=[-5, 5], ylim=[0, .])