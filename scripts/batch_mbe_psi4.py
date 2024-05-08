#!/usr/bin/python3

import numpy as np
import subprocess
import os
import datetime
import glob

DFT_METHOD = 'b3lyp'
BASIS = '6-31G*'

N = 3 # no. of monomers in the cluster, N <= 25 at this time
#GEOM_FILE = 'W'+str(N)+'_geoms_all.xyz'
GEOM_FILE = '3random_waters-100.xyz'
#GEOM_FILE = 'W3_subgeoms_from_4_5.xyz'
#GEOM_FILE = 'W3-test.xyz'
NAME_DECOR = "_random_"
#NAME_DECOR = "_sub3f_4_5" # "-" is not allowed in Psi4 calculations
#NAME_DECOR = "_test_"
#NO_CLUSTERS = "230"
NO_CLUSTERS = "100"
DELETE_SCRATCH = True # if false keeping the scratch files for debugging purpose
TIME_FILE = "calc_timer.txt" # record the calculation time

GREEK_NUMBER_PREFIX = {
        1:'momo',
        2:'di',
        3:'tri',
        4:'tetra',
        5:'penta',
        6:'hexa',
        7:'hepta',
        8:'octo',
        9:'ennea',
        10:'deca',
        11:'hendeca',
        12:'dodeca',
        13:'triadeca',
        14:'tessaradeca',
        15:'pentedeca',
        16:'hexadeca',
        17:'heptadeca',
        18:'octodeca',
        19:'enneadeca',
        20:'icosi',
        21:'icosikaihena',
        22:'icosidi',
        23:'icositri',
        24:'icositetra',
        25:'icosipenta'
        }

CLUSTER_NAME = GREEK_NUMBER_PREFIX[N]+'mer'+NAME_DECOR+NO_CLUSTERS

DISPERSION_CORRECTION = 'd3' # options = 'nodc' or 'd3' at this time, should have 'd4'
DC = '' if (DISPERSION_CORRECTION == 'nodc') else '-'+DISPERSION_CORRECTION

BSSE_TYPE = 'vmfc' # psi4 options: 'vmfc', 'cp', 'nocp'
MAX_NBODY = np.minimum(N,4)

# read all geoms in and store them into an array
# one geom into one row

#geom = [[]] 

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
            label.append(CLUSTER_NAME+"-"+str(i+1))
            if i != 0:
                geom = np.vstack([geom,geom_blank])
        elif len(line_sp) == 4:
            if i == 0:
                geom[j:j+4] = line_sp
            else:
                geom[i,j:j+4] = line_sp
            j += 4

with open(CLUSTER_NAME+'-MBE.out', 'w') as MBEOut:
    MBEOut.write("Many-body Expansion Energies of Water {}s\n".format(CLUSTER_NAME))
    MBEOut.write("Calculation settings: {} {} {} {}\n".format(DFT_METHOD,BASIS,DISPERSION_CORRECTION,BSSE_TYPE))
    MBEOut.write("Results are listed as columns of Total Energy, Interaction Energy and N-body contribution at different expansion orders in Eh.\n\n")
    for ii in range(len(label)):
        with open('tmp-psi4-'+str(ii)+'.in', 'w') as PsiInp:
            PsiInp.write("molecule {} {{\n".format(CLUSTER_NAME))
            for j in range(0,row_length,4):
                PsiInp.write("{} {} {} {}\n".format(geom[ii,j],geom[ii,j+1],geom[ii,j+2],geom[ii,j+3]))
                if ((j+4)%12 == 0 and ((j+4) < row_length)):
                    PsiInp.write("--\n")
            PsiInp.write("}\n")
            PsiInp.write("\n")
            PsiInp.write("set basis {}\n".format(BASIS))
            PsiInp.write("\n")
            PsiInp.write("ecp = {}\n")
            PsiInp.write("\n")
            PsiInp.write("label = \'{}\'\n".format(label[ii]))
            PsiInp.write("\n")
            PsiInp.write("ecp[label] = energy(\'{}\', bsse_type = \'{}\', max_nbody = {})\n".format(DFT_METHOD+DC, BSSE_TYPE, MAX_NBODY))
    
        subprocess.run(["psi4", 'tmp-psi4-'+str(ii)+'.in', 'tmp-psi4-'+str(ii)+'.out']) # run the Psi4 MBE calculation

        MBEOut.write("{}\n".format(label[ii]))

        with open('tmp-psi4-'+str(ii)+'.out', 'r') as PsiOut:
            for line in PsiOut:
                if line.startswith("        n-Body"):
                    PsiOut.readline()
                    line_sp = PsiOut.readline().split()
                    kk = 0
                    while len(line_sp) != 0:
                        kk += 1
                        if kk > MAX_NBODY:
                            break
                        if (line_sp[0] == 'FULL/RTN') or (line_sp[0] == 'RTN'):
                            MBEOut.write("{} {} {}\n".format(line_sp[2],line_sp[3],line_sp[5]))
                        else:
                            MBEOut.write("{} {} {}\n".format(line_sp[1],line_sp[2],line_sp[4]))
                        line_sp = PsiOut.readline().split()
                    MBEOut.write("\n")

if DELETE_SCRATCH:
    for f in glob.glob("tmp-psi4*"):
        os.remove(f)

end_time = datetime.datetime.now()

with open(TIME_FILE, "w") as time_file:
    time_file.write("Calculation begins on: {}\n".format(begin_time))
    time_file.write("Calculation ends on: {}\n".format(end_time))
    time_file.write("Calculation running time: {}".format(str(datetime.timedelta(seconds = (end_time - begin_time).total_seconds()))))
