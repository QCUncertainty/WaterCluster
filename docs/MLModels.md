# Building Machine Learning Models on the Uncertainties of Many-body Expansion Energies at Different Orders

Our target in this LDRD project is to build machine learning (ML) models to predict the uncertainties of the Many-body expansion (MBE) energies of water clusters. These models should be useful in studying the energetics of various water clusters. In addition, the protocol of building such ML models should be general to investigate any molecular cluster or molecular aggregate systems.

## Generating Big Data of Water Cluster Energetics

### Water Cluster Structures

We want to have many water cluster structures which are able to represent the full atomic coordinate space of water clusters of different sizes. To achieve this goal, we obtain the water cluster structures in different ways:
1. **Generating water clusters randomly in a box.** 
   We develop Python scripts to randomly put user-defined number of water molecules into a box ([see the doc about the scripts](https://github.com/QCUncertainty/WaterCluster/blob/main/README.md)), of which the size is also user-defined. For each water molecule, the geometric elements (bond length and bond angle) are normally distributed around experimental reference values (the expectation value and variance of this normal distribution can be adjusted by the user).
2. **Extracting fragment structures from a database of minimum energy water cluster structures.**  
   Rakshit et al. built a database of minimum energy water cluster structures using the TTM2.1-F ab-initio based interaction potential [^Ref1]. All cluster minima with of the no. of water molecules n = 3 – 30 can be downloaded from the link: https://drive.google.com/file/d/18Y7OiZXSCTsHrQ83GCc4fyE_abbL6E_n/view?usp=sharing. For small water clusters, such as n = 3 - 5, the no. of such minimum energy structures are not many (there are only 2, 10 and 19 structures, respectively), so more structures are generated from the fragment structures of larger water clusters. For example, more water pentamers can be generated from deleting two water molecules from all heptamers. We have developed Python scripts to finish this job ([see the doc about the scripts](https://github.com/QCUncertainty/WaterCluster/blob/main/README.md)).
3. Generating water clusters from the snapshots of molecular dynamics (MD) simulation trajectories. In principle, one can put a certain number of water molecules into a box and run MD simulations. The snapshots of the MD trajectories can be accepted as water cluster structure samples. Since we have generated sufficiently many water clusters through 1. and 2., we have not go into this direction yet.
   
No one knows through which way one could obtain sample water cluster structures better representing the full atomic coordination space. We need numerical evidence to check the generated water cluster structures.

### MBE Energies from High Throughput Calculations
We have two types of solutions to run the high throughput MBE calculations. One is the local machine solution in which all MBE calculations are run on a local Linux box; while in the other server/client solution one relies on the QCFractal/QCManybody package to set up and run data/compute servers and clients ([see the doc about QCArchive/QCFractal/QCManybody](https://github.com/QCUncertainty/WaterCluster/blob/main/docs/QCFractal.md)). The local machine solution is easy to apply but cannot scale. Another drawback of the local machine solution is that it requires a quantum chemistry package supporting the MBE calculations, which reduces the number of choices. The server/client solution is systematic and can be applied to any generic high throughput quantum chemistry calculations. Moreover, MBE calculations is coded in the QCArchive/QCFractal/QCManybody package, so that any quantum chemistry package which can calculate the total energy of a molecular system can be used as a calculation engine. However, the QCArchive/QCFractal/QCManybody package is still under development. Bugs are not rare and the documentation is still limited, which makes setting up and running the server/client not an easy task.
1. **Local machine solution**
   We developed a Python script to batch run MBE calculations on water cluster coordinates stacked in a .xyz file ([see the doc about the scripts](https://github.com/QCUncertainty/WaterCluster/blob/main/README.md)). Currently Psi4 is used as the quantum chemistry engine. The Python script reads the water cluster structure one-by-one, and generate a temporary Psi4 input file for the MBE calculation, then the MBE calculation is run as a subprocess. Now the MBE calculations on different water clusters are not running in parallel, which does not use up the multicore of multithread computing power. The next step to improve the performance of this batch run script is to add multithreading function.
2. **Server/Client solution**
   In the server/client solution, a QCFractal data server is set up to store and manage the calculation results. A QCFractal compute server is alsoe set up to handle the calculations. The user installs the QCArchive/QCFractal/QCManybody packages on his local machine and the local machine works as a client. In a MBE calculation task, the user first login to the data server and establish the data connection between the server and the calculation, then the user submits a job to the compute server. On a high-performance computer, the compute server ditributes the calculation tasks into different calculation nodes. When the calculations are done, the results are collected and stored in the data server for future reference and analysis. How to set up the compute server depends on the hardware/software environment of the specific computing resource used (Nova?), which is still under investigation (Dullitha). For a quick warm-up, please see the doc on [setting up the servers on a local machine](https://github.com/QCUncertainty/WaterCluster/blob/main/docs/QCFractal.md).


## ML Models on MBE Energies

### Descriptors

### Neural Network (NN) Models

### Gaussian Process Regression (GPR) Models

[^Ref1]: Avijit Rakshit and Pradipta Bandyopadhyay, Joseph P. Heindel and Sotiris S. Xantheas “Atlas of putative minima and low-lying energy networks of water clusters n=3-25”, *J. Chem. Phys.* **151**, 214307 (2019).