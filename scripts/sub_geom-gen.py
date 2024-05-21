#!/usr/bin/python3

import numpy as np
import itertools

N = 6 # no. of monomers in the original cluster, N <= 30 at this time
GEOM_FILE = 'W'+str(N)+'_geoms_all.xyz'

L = 3 # no. of monomers in the subsctructures of the original cluster, 0< L < N
SUB_GEOM_FILE = 'W'+str(L)+'_subgeoms_from_'+str(N)+'.xyz'

i = -1

row_length = 12*N # no. of elements for a geom row of a structure

geom_blank = ["012345678912345678"]*row_length # the length of this string must be greater
                                               # than the longest coordinate number in the
                                               # original .xyz file. Otherwise the coordinate
                                               # number will be cut short and thus cause hidden 
                                               # problems.
geom = [geom_blank]

j = 0
with open(GEOM_FILE,'r') as Inp:
    for line in Inp:
        line_sp = line.split()
        if len(line_sp) == 1:
            i += 1
            j = 0
            if i != 0:
                geom = np.vstack([geom,geom_blank])
        elif len(line_sp) == 4:
            if i == 0:
                geom[j:j+4] = line_sp
            else:
                geom[i,j:j+4] = line_sp
            j += 4

kk = 1

with open(SUB_GEOM_FILE, 'w') as SUBOut:
    for i in range(len(geom)):
        if isinstance(geom[0],str):
            rsh_geom = np.asarray(geom).reshape(N,12)
        else:
            rsh_geom = geom[i].reshape(N,12)
        sub_geom = []
        for sub in itertools.combinations(rsh_geom, L):
            tmp = []
            for mono in sub:
                tmp.append(mono.tolist())
            sub_geom.append(sum(tmp,[]))
        for j in range(len(sub_geom)):
            SUBOut.write("{}\n".format(3*L))
            SUBOut.write("substructure {}-mer {} from {}-mer\n".format(L,kk,N)) 
            kk += 1
            k = 0
            for jj in sub_geom[j]:
                SUBOut.write("{} ".format(jj))
                k += 1
                if k%4 == 0:
                    SUBOut.write("\n")
                    k = 0
