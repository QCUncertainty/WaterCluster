#!/usr/bin/python3

import numpy as np
import subprocess
import os
import datetime
import glob
import shutil

DFT_METHOD = 'b3lyp'
BASIS = '6-31G*'

N = 1
GEOM_FILE = 'random_water_mono-100.xyz'
NAME_DECOR = "random_water_"
#NAME_DECOR = "_sub3f_4_5_" # "-" is not allowed in Psi4 calculations
NO_MOLS = "100"
DELETE_SCRATCH = True # if false keeping the scratch files for debugging purpose
TIME_FILE = "calc_timer.txt" # record the calculation time

MOL_NAME = NAME_DECOR+NO_MOLS

DISPERSION_CORRECTION = 'd3' # options = 'nodc' or 'd3' at this time, should have 'd4'
DC = '' if (DISPERSION_CORRECTION == 'nodc') else '-'+DISPERSION_CORRECTION

# read all geoms in and store them into an array
# one geom into one row

label = [] # labels of the geoms

i = -1

row_length = 12*N # no. of elements for a geom row of a structure

geom_blank = [" "]*row_length
geom = [geom_blank]

j = 0

begin_time = datetime.datetime.now()

with open(GEOM_FILE,'r') as Inp:
    for line in Inp:
        line_sp = line.split()
        if len(line_sp) == 1:
            i += 1
            j = 0
            label.append(MOL_NAME+"-"+str(i+1))
            if i != 0:
                geom = np.vstack([geom,geom_blank])
        elif len(line_sp) == 4:
            if i == 0:
                geom[j:j+4] = line_sp
            else:
                geom[i,j:j+4] = line_sp
            j += 4

with open(MOL_NAME+'-sp.out', 'w') as SPOut:
    SPOut.write("Single Point Energies of {}\n".format(MOL_NAME))
    SPOut.write("Calculation settings: {} {} {}\n".format(DFT_METHOD,BASIS,DISPERSION_CORRECTION))
    for ii in range(len(label)):
        with open('tmp-psi4-sp'+str(ii)+'.in', 'w') as PsiInp:
            PsiInp.write("molecule {} {{\n".format(MOL_NAME))
            for j in range(0,row_length,4):
                PsiInp.write("{} {} {} {}\n".format(geom[ii,j],float(geom[ii,j+1]),float(geom[ii,j+2]),float(geom[ii,j+3])))
            PsiInp.write("}\n")
            PsiInp.write("\n")
            PsiInp.write("set basis {}\n".format(BASIS))
            PsiInp.write("\n")
            PsiInp.write("energy(\'{}\')\n".format(DFT_METHOD+DC))
    
        subprocess.run(["psi4", 'tmp-psi4-sp'+str(ii)+'.in', 'tmp-psi4-sp'+str(ii)+'.out']) # run the Psi4 single point energy calculation

        SPOut.write("{}\t".format(label[ii]))
        last_line = []
        with open('tmp-psi4-sp'+str(ii)+'.out', 'r') as PsiOut:
            for line in PsiOut:
                if line.startswith("    Total Energy ="):
                    line_sp = line.split()
                    SPOut.write("{}\n".format(line_sp[3]))
                last_line = line
# keep the not successful output files
        if "successfully" not in last_line:
            shutil.copyfile('tmp-psi4-sp'+str(ii)+'.out', 'tmp-psi4-sp'+str(ii)+'.err')

if DELETE_SCRATCH:
    for f in glob.glob("tmp-psi4*.in"):
        os.remove(f)
    for f in glob.glob("tmp-psi4*.out"):
        os.remove(f)
    for f in glob.glob("tmp-psi4*.log"):
        os.remove(f)

end_time = datetime.datetime.now()

with open(TIME_FILE, "w") as time_file:
    time_file.write("Calculation begins on: {}\n".format(begin_time))
    time_file.write("Calculation ends on: {}\n".format(end_time))
    time_file.write("Calculation running time: {}".format(str(datetime.timedelta(seconds = (end_time - begin_time).total_seconds()))))
