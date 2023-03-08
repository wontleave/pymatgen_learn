from ase.io import read, write
from ase.units import kg, m, _amu
import numpy as np
from pathlib import Path
from os import path
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate the density from a PBC calculation')
    parser.add_argument('--path', help='path to the MD trajectory files. E.g. XDATCAR')
    parser.add_argument('--write_to', help="path to write the separated molecule", default=None)
    args = parser.parse_args()
    path_ = args.path
    ensemble = read(path_, index=":")
    if args.write_to is None:
        root_path = path.dirname(path_)
    else:
        root_path = args.write_to
    for idx in range(0, len(ensemble), 50):
        folder_path = Path(path.join(root_path, f"{idx}"))
        folder_path.mkdir(parents=True, exist_ok=True)
        write(path.join(folder_path, "POSCAR"), ensemble[idx])