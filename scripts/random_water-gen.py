# python script to generate randomly positioned and oriented n-water clusters 
# in a designated box.
# Usage: modify the setting lines below and run `python random_water-gen.py`

import numpy as np
import random as rd

def read_water_model(INPUT):
    # O atom at the origin
    arr = []
    with open(INPUT,'r') as WATER_in:
        for line in WATER_in:
            line_sp = line.split()
            if len(line_sp) == 4:
                for ii in line_sp[1:]:
                    arr.append(float(ii))

    arr = np.reshape(arr, (3,3))
    # water coordinates are in the row vectors of arr
    return arr

# random rotation matrix
# alpha, beta and gamma are random rotation angles
def rot(alpha, beta, gamma):
    R11 = np.cos(alpha)*np.cos(beta)
    R12 = np.cos(alpha)*np.sin(beta)*np.sin(gamma) - np.sin(alpha)*np.cos(gamma)
    R13 = np.cos(alpha)*np.sin(beta)*np.cos(gamma) + np.sin(alpha)*np.sin(gamma)
    R21 = np.sin(alpha)*np.cos(beta)
    R22 = np.sin(alpha)*np.sin(beta)*np.sin(gamma) + np.cos(alpha)*np.cos(gamma)
    R23 = np.sin(alpha)*np.sin(beta)*np.cos(gamma) - np.cos(alpha)*np.sin(gamma)
    R31 = -np.sin(beta)
    R32 = np.cos(beta)*np.sin(gamma)
    R33 = np.cos(beta)*np.cos(gamma)
    return np.array([[R11, R12, R13],
            [R21, R22, R23],
            [R31, R32, R33]])

def random_rot_water(water0):
    alpha = rd.random() * 2.0 * np.pi
    beta = rd.random() * 2.0 * np.pi
    gamma = rd.random() * 2.0 * np.pi
    R_mat = rot(alpha, beta, gamma)
    # coordinates in the row vectors
    return np.transpose(np.matmul(R_mat, np.transpose(water0)))

# generate a random point in a box
def random_point(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        raise Exception("Box dimensions must be positive!")
    aa = rd.random() * a
    bb = rd.random() * b
    cc = rd.random() * c
    return [aa, bb, cc]

# put a water molecule at some random postion in a box 
# and with some random orientation
def random_water(water0, a, b, c):
    pos = random_point(a, b, c)
    # get the model water coordinates
    #water0 = read_water_model(WaterFile)
    # rotate the water molecule with some random angles
    water = random_rot_water(water0)
    # move the O atom of the water molecule to the random position
    for i in range(3):
        water[i] += pos

    return water

# calculate the distance between two atoms, in angstrom
def atom_dist(atom1, atom2):
    return np.sqrt((atom1[0] - atom2[0])**2 + (atom1[1] - atom2[1])**2 + (atom1[2] - atom2[2])**2)

# determine if the new atoms are too close
# to already positioned water molecules
def close_atoms(waters, water):
    n_waters = len(waters)
    # only need to check the last added water
    for i in range(n_waters):
        for atom in waters[i]:
            if atom_dist(atom,water[0]) < 1.52:
                return True
            if atom_dist(atom,water[1]) < 1.2:
                return True
            if atom_dist(atom,water[2]) < 1.2:
                return True
    return False

# whether the water molecule is in the box
def in_box(water, a, b, c):
    tmp = np.transpose(water)
    for xx in tmp[0]:
        if xx < 0 or xx > a:
            return False
    for yy in tmp[1]:
        if yy < 0 or yy > b:
            return False
    for zz in tmp[2]:
        if zz < 0 or zz > c:
            return False
    return True

# settings
WATER_FILE = 'water.xyz'
M = 100 # no. of water cluster structures
N = 3 # no. of water molecules in the box
a = 5
b = 5
c = 5 # dimensions of the box, in angstrom
OUTPUT = str(N)+'random_waters-'+str(M)+'.xyz'

# generate the coordinates of N random water molecules
water0 = read_water_model(WATER_FILE)

# clean the output file before writing
open(OUTPUT, 'w').close()

# run M times
for jj in range(M):
    waters = []
    ii = 0
    
    while True:
        # get a randomly positioned water
        water = random_water(water0, a, b, c)
        if not in_box(water, a, b, c):
            print("Water out of box! Reposition.")
            continue
        if ii ==  0:
            waters.append(water)
            ii += 1
        else:
            if close_atoms(waters, water):
                # re-position the water molecule if some atoms are too close
                print("Atoms too close! Reposition the water molecule.")
                continue
            else:
                waters.append(water)
                ii += 1
        if ii >= N:
            break
    
    # write output
    with open(OUTPUT, 'a') as WATER_out:
        ii = 0
        for water in waters:
            if ii == 0:
                WATER_out.write("{}\n".format(N*3))
                WATER_out.write("{} randomly positioned water molecules in a {} * {} * {} box.\n".format(N,a,b,c))
                ii = 1
            WATER_out.write("O {} {} {}\n".format(water[0,0], water[0,1], water[0,2]))
            WATER_out.write("H {} {} {}\n".format(water[1,0], water[1,1], water[1,2]))
            WATER_out.write("H {} {} {}\n".format(water[2,0], water[2,1], water[2,2]))
