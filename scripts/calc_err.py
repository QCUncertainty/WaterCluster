import numpy as np

# Setting
RESULT_FILE = "trimer_random_50_50-MBE.out"
N = 3
max_nbody = 3
ERR_FILE = "trimer_random_50-err.out"
# End Setting

energies = []

with open(RESULT_FILE, "r") as INPUT:
    for line in INPUT:
        line_sp = line.split()
        if len(line_sp) == 1:
            energy = []
            for i in range(max_nbody):
                line_tmp = INPUT.readline()
                line_tmp_sp = line_tmp.split()
                energy.append(float(line_tmp_sp[0]))
            energies.append(energy)

with open(ERR_FILE, "w") as OUTPUT:
    for energy in energies:
        for i in range(max_nbody-1):
            OUTPUT.write("{}   ".format(energy[i] - energy[-1]))
        OUTPUT.write("\n")

