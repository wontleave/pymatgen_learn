from ase.io import read, write
from ase.build import sort
from pymatgen.io.vasp import Vasprun
# from flare.dft_interface.vasp_util import md_trajectory_from_vasprun
# from flare.gp import GaussianProcess
# from flare.gp_from_aimd import TrajectoryTrainer
import pickle
from os import path

if __name__ == "__main__":
    xml_path = r"C:\Users\wontl\PycharmProjects\flare_training\mes_h2o_pentaCl\vasprun.xml"
    pick_path = r"C:\Users\wontl\PycharmProjects\flare_training\mes_h2o_pentaCl\vasprun.xml.pickle"

    # trajectory = md_trajectory_from_vasprun(xml_path)
    #
    # with open(pick_path, "wb") as f:
    #     pickle.dump(trajectory, f)
    #     print("Pickled vasprun.xml! Done")

    # with open(pick_path, "rb") as f:
    #     trajectory = pickle.load(f)
    #
    # trimmed_traj = trajectory[::5]
    # Extended XYZ to POSCAR

    root = r"E:\calc_results\packmol_scratch\MeOH_aq_cube"

    structure = read(path.join(root, "aq_MeOH80vv.xyz"))
    write(path.join(root, "POSCAR"), sort(structure))
    # write(path.join(root, "toluenes.dat"), sort(structure), format="lammps-data")
    # CIF to POSCAR
    # full_filename = r"E:\calc_results\CaF2\CaF2_mp-2741_conventional_standard.cif"
    # structure = read(full_filename)
    # write(r"E:\calc_results\CaF2\POSCAR", structure)
    ## Setup the Gaussian Processes of Flare
    # hyper_pars = [0.01, 0.01, 0.01, 0.01, 0.01]
    # cut_offs = { "twobody": 7.0, "threebody": 3.0}
    # hyper_pars_labels = ['Two-Body Signal Variance','Two-Body Length Scale','Three-Body Signal Variance',
    #                      'Three-Body Length Scale', 'Noise Variance']
    # gp = GaussianProcess(kernels=["twobody", "threebody"],
    #                      hyps=hyper_pars, cutoffs=cut_offs, hyp_labels=hyper_pars_labels,
    #                      parallel=True, per_atom_par=True, n_cpus=2)
    #
    # # Using the TrajectoryTrainer
    # training = TrajectoryTrainer(frames=trajectory,
    #                              gp=gp,
    #                              rel_std_tolerance=3,
    #                              abs_std_tolerance=0,
    #                              pre_train_on_skips=5,
    #                              pre_train_atoms_per_element={"H": 5, "O": 5, "Cl": 1, "N": 5, "C": 10},
    #                              train_atoms_per_element={"H": 20, "O": 20, "Cl": 1, "N": 5, "C": 25}, validate_ratio=0.3)

    # training.run()
    print("Done")