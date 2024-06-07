from pymatgen.io.vasp.outputs import Vasprun
import os
import numpy as np

"""
Run subfolders that contain ionic relaxation jobs in a root folder
"""


def list_subfolders(root_folder, filename=r"OPT\vasprun.xml"):
    try:
        subfolders_with_file = []
        for name in os.listdir(root_folder):
            subfolder_path = os.path.join(root_folder, name)
            if os.path.isdir(subfolder_path) and os.path.isfile(os.path.join(subfolder_path, filename)):
                subfolders_with_file.append(subfolder_path)
        return subfolders_with_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    root_path = r"E:\calc_results\PtNi_nanowire\Pt_FCC\111\OPT\MeOH_ads"
    subfolders = list_subfolders(root_path)
    filename = r"OPT\vasprun.xml"

    vasp_jobs = []
    for i, subfolder in enumerate(subfolders):
        print(subfolder)
        vasp_jobs.append(Vasprun(os.path.join(subfolder, filename)))
        print(vasp_jobs[i].converged)


    energies = np.array([vasp_jobs[i].final_energy for i in range(len(vasp_jobs))])
    # rel_energies = (energies - np.min(energies)) * 23.0606548
    # print(rel_energies)

    slab_path = r"E:\calc_results\PtNi_nanowire\Pt_FCC\111"
    slab_job = Vasprun(os.path.join(slab_path, filename))

    ads_path = r"E:\calc_results\PtNi_nanowire\Adsorbate\MeOH"
    abs_jobs = Vasprun(os.path.join(ads_path, filename))

    ads_energy = energies[np.argmin(energies)] - slab_job.final_energy - abs_jobs.final_energy
    print(f"Slab + ads = {energies[np.argmin(energies)]}")
    print(f"Slab energy = {slab_job.final_energy}")
    print(f"adsorbate energy = {abs_jobs.final_energy}")
    print(f"Adsorption energy = {ads_energy}")