import numpy as np
import random as rd
import os

# Settings
GEOM_FILE = 'W5_subgeoms_from_7.xyz'
select_no = 1000 # no. of selected geoms
OUT_FILE = 'sub5_f7_rand_selc-1000.xyz'
DELETE_SCRATCH = True # if false keeping the scratch files for debugging purpose

# End settings

with open(GEOM_FILE, 'r') as INPUT:
    no_atoms = int(INPUT.readline())
    cluster_no_lines = no_atoms + 2
    no_lines = len(INPUT.readlines()) + 1
    no_cluster = int(no_lines/cluster_no_lines)

# generate a list of indices to label the clusters
idx_list = rd.sample(range(0, no_cluster + 1), select_no)

# function to extract a cluster geom with the index
def geom_extract(FILE, index):
    start_line = cluster_no_lines * index
    with open(FILE, 'r') as INPUT:
        lines = INPUT.readlines()
        with open('cluster.tmp','w') as OUT:
            for i in range(start_line, start_line + cluster_no_lines):
                OUT.write(lines[i])

# randomly select some geoms from the cluster geom file
# clear output file if existed
with open(OUT_FILE, 'w') as OUT:
    pass
    
with open(OUT_FILE, 'a') as OUT:
    for i in idx_list:
        geom_extract(GEOM_FILE,i)
        with open('cluster.tmp','r') as TMP:
            OUT.write(TMP.read())

if DELETE_SCRATCH:
    os.remove("cluster.tmp")

