# WaterCluster
This repo contains the codes and data of many-body expansion calculations on water clusters.

Notes on the files:
- scripts/batch_mbe_psi4.py: python script to batch run MBE calculations with Psi4.
- scripts/sub_geom-gen.py: python script to generate smaller clusters from larger clusters.
- scripts/random_water-gen.py: python script to generate water clusters with water molecules randomly positioned and oriented in a designated box.
- scripts/err_distr.ipynb: jupyter notebook to analyze the MBE errors.
- scripts/sp_dataset.ipynb: jupyter notebook to create a singlepoint energy calculation dataset.
- scripts/mbe_dataset.ipynb: jupyter notebook to create a many-body expansion calculation dataset.
- scripts/calc_err.py: python script to extract MBE energies from \*MBE.out and calculate errors relative to the full body energy.
- scripts/mono_water_gen.py: python script to generate a water with the bond lengths and bond angle in defined normal distributions.
- scripts/batch_sp_psi4.py: python script to batch run single point energy calculations with Psi4.
- geoms/Wn_geoms_all.xyz (n = 3 - 10): stacked xyz files of n-water clusters (n = 3 - 10). Structures are from the database at https://sites.uw.edu/wdbase/database-of-water-clusters/.
- geoms/water.xyz: model water molecular coordinates for more water cluster geometries generation.
- geoms/W3_subgeoms_from_4_5.xyz: water trimer geometries as substructrures from W4_geoms_all.xyz and W5_geoms_all.xyz. Generated with sub_geom-gen.py.
- geoms/3random_waters-100.xyz: water trimers randomly positioned and oriented in a 5 * 5 * 5 (angstrom) box. Generated with random_water-gen.py and water.xyz.
- data_results/example-trimer-psi4-MBE.out: The Psi4 output file of an example trimer MBE calculation.
- data_results/trimer_random_100-MBE.out: Psi4 MBE calculation results with the geometries in 3random_waters-100.xyz.
- data_results/trimer_sub3f_4_5-230-MBE.out: Psi4 MBE calculation results with the geometries in W3_subgeoms_from_4_5.xyz.
- data_results/trimer-rand100-MBE2-b3lyp_d3-631gdp.png: histogram plot of MBE (n = 2) errors calcuated using the results in trimer_random_100-MBE.out.
- data_results/trimer-subgeom3_f4_5-MBE2-b3lyp_d3-631gdp.png: histogram plot of MBE (n = 2) errors calcuated using the results in trimer_sub3f_4_5-230-MBE.out.
