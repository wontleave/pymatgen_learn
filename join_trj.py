from ase.io import read, write
from ase.units import kg, m, _amu
import numpy as np
import matplotlib.pylab as plt
from pathlib import Path
from os import path, listdir
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine a series of trajectories')
    parser.add_argument('--root', help='path to the root folders with subfolders that contain the trajectories')
    parser.add_argument('--write_to', help="path to write the separated molecule", default=None)
    args = parser.parse_args()

    all_folders = listdir(args.root)
    trajectories = {}
    for folder in all_folders:
        full_path = path.join(args.root, folder)
        full_path = path.join(full_path, "vasprun.xml")
        print(full_path)
        _, idx = folder.split("R")
        trajectories[int(idx)] = read(full_path, index=":")

    all_trajectories = []
    trajectories = {k: trajectories[k] for k in sorted(trajectories)}

    for key in trajectories:
        all_trajectories += trajectories[key]

    energies = np.array([i.get_potential_energy() for i in all_trajectories])
    plt.plot(energies)
    plt.ylabel("Potential Energy (eV)")
    plt.show()