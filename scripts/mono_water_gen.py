# python script to generate water structures of which the bond length/angle
# distribute normally around the reference values.
# Usage: modify the setting lines below and run `python mono_water_gen.py`

import numpy as np
import random as rd

# generate the coordinates of O, H1, H2
# bl1,2: bond lengths in angtrom; ba: bond angle in degree
# O is always at the origin
# The molecule is on the xy plane
def water_geom(bl1, bl2, ba):
    coords = []
    coords.append([0.0, 0.0, 0.0])
    coords.append([-bl1*np.sin(ba*np.pi/360.0), bl1*np.cos(ba*np.pi/360.0), 0.0])
    coords.append([bl2*np.sin(ba*np.pi/360.0), bl2*np.cos(ba*np.pi/360.0), 0.0])

    return coords

# generate a random number acoording to the normal distribution defined
# center = expectation value; 3*sigma = center * frac%
def rd_normal(center, frac):
    sigma = center * frac/300.0
    return np.random.normal(loc=center, scale=sigma)


# Settings
bond_length = 0.9572
bond_angle = 104.5
frac = 10

N = 100 # no. of monomer geoms generated
NAME_DECOR = "-train"

OUTPUT_FILE = 'random_water_mono-'+str(N)+NAME_DECOR+'.xyz'
DESCR_FILE = 'random_water_mono-'+str(N)+NAME_DECOR+'-geom.dat'

# END Settings

with open(DESCR_FILE, "w") as DescrFile:
    with open(OUTPUT_FILE, "w") as OutFile:
        for i in range(N):
            OH1 = rd_normal(bond_length, frac)
            OH2 = rd_normal(bond_length, frac)
            HOH = rd_normal(bond_angle, frac)
            DescrFile.write("{}\t{}\t{}\n".format(OH1,OH2,HOH))
            coords = water_geom(OH1, OH2, HOH)
            OutFile.write("3\n")
            OutFile.write("random water geometry No. "+str(i+1)+"\n")
            for j in range(3):
                if j == 0:
                    OutFile.write("O    {}  {}  {}\n".format(coords[0][0], coords[0][1], coords[0][2]))
                else:
                    OutFile.write("H    {}  {}  {}\n".format(coords[j][0], coords[j][1], coords[j][2]))
    


