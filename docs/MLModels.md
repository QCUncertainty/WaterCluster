# Building Machine Learning Models on the Uncertainties of Many-body Expansion Energies at Different Orders

Our target in this LDRD project is to build machine learning (ML) models to predict the uncertainties of the Many-body expansion (MBE) energies of water clusters. These models should be useful in studying the energetics of various water clusters. In addition, the protocol of building such ML models should be general to investigate any molecular cluster or molecular aggregate systems.

## Generating Big Data of Water Cluster Energetics

### Water Cluster Structures

We want to have many water cluster structures which are able to represent the full atomic coordinate space of water clusters of different sizes. To achieve this goal, we obtain the water cluster structures in different ways:
1. **Generating water clusters randomly in a box.** 
   We develop Python scripts to randomly put user-defined number of water molecules into a box ([see the doc about the scripts](https://github.com/QCUncertainty/WaterCluster/blob/main/README.md)), of which the size is also user-defined. For each water molecule, the geometric elements (bond length and bond angle) are normally distributed around experimental reference values (the expectation value and variance of this normal distribution can be adjusted by the user).
2. **Extracting fragment structures from a database of minimum energy water cluster structures.**  
   Rakshit et al. built a [database](https://sites.uw.edu/wdbase/database-of-water-clusters/) of minimum energy water cluster structures using the TTM2.1-F ab-initio based interaction potential [^Ref1]. All cluster minima with of the no. of water molecules n = 3 – 30 can be downloaded from the link: https://drive.google.com/file/d/18Y7OiZXSCTsHrQ83GCc4fyE_abbL6E_n/view?usp=sharing. For small water clusters, such as n = 3 - 5, the no. of such minimum energy structures are not many (there are only 2, 10 and 19 structures, respectively), so more structures are generated from the fragment structures of larger water clusters. For example, more water pentamers can be generated from deleting two water molecules from all heptamers. We have developed Python scripts to finish this job ([see the doc about the scripts](https://github.com/QCUncertainty/WaterCluster/blob/main/README.md)).
3. Generating water clusters from the snapshots of molecular dynamics (MD) simulation trajectories. In principle, one can put a certain number of water molecules into a box and run MD simulations. The snapshots of the MD trajectories can be accepted as water cluster structure samples. Since we have generated sufficiently many water clusters through 1. and 2., we have not go into this direction yet.
   
No one knows through which way one could obtain sample water cluster structures better representing the full atomic coordination space. We need numerical evidence to check the generated water cluster structures.

### MBE Energies from High Throughput Calculations
We have two types of solutions to run the high throughput MBE calculations. One is the local machine solution in which all MBE calculations are run on a local Linux box; while in the other server/client solution one relies on the QCFractal/QCManybody package to set up and run data/compute servers and clients ([see the doc about QCArchive/QCFractal/QCManybody](https://github.com/QCUncertainty/WaterCluster/blob/main/docs/QCFractal.md)). The local machine solution is easy to apply but cannot scale. Another drawback of the local machine solution is that it requires a quantum chemistry package supporting the MBE calculations, which reduces the number of choices. The server/client solution is systematic and can be applied to any generic high throughput quantum chemistry calculations. Moreover, MBE calculations is coded in the QCArchive/QCFractal/QCManybody package, so that any quantum chemistry package which can calculate the total energy of a molecular system can be used as a calculation engine. However, the QCArchive/QCFractal/QCManybody package is still under development. Bugs are not rare and the documentation is still limited, which makes setting up and running the server/client not an easy task.
1. **Local machine solution**
   We developed a Python script to batch run MBE calculations on water cluster coordinates stacked in a .xyz file ([see the doc about the scripts](https://github.com/QCUncertainty/WaterCluster/blob/main/README.md)). Currently Psi4 is used as the quantum chemistry engine. The Python script reads the water cluster structure one-by-one, and generate a temporary Psi4 input file for the MBE calculation, then the MBE calculation is run as a subprocess. Now the MBE calculations on different water clusters are not running in parallel, which does not use up the multicore of multithread computing power. The next step to improve the performance of this batch run script is to add multithreading function.
2. **Server/Client solution**
   In the server/client solution, a QCFractal data server is set up to store and manage the calculation results. A QCFractal compute server is alsoe set up to handle the calculations. The user installs the QCArchive/QCFractal/QCManybody packages on his local machine and the local machine works as a client. In a MBE calculation task, the user first login to the data server and establish the data connection between the server and the calculation, then the user submits a job to the compute server. On a high-performance computer, the compute server ditributes the calculation tasks into different calculation nodes. When the calculations are done, the results are collected and stored in the data server for future reference and analysis. How to set up the compute server depends on the hardware/software environment of the specific computing resource used (Nova?), which is still under investigation (Dullitha). For a quick warm-up, please see the doc on [setting up the servers on a local machine](https://github.com/QCUncertainty/WaterCluster/blob/main/docs/QCFractal.md).

Currently both Psi4 and QCManybody do not support total energy evaluations in truncated MBE calculations, so in order to evaluate the MBE errors one need to run separated single point energy calculations.


## ML Models on MBE Energies
We want to design ML models to predict MBE energies as well as the uncertainty of the predictions. We think this MBE energy fitting task is similar to constructing ML-based potential energy surfaces (PES) [^Ref2] or force fields [^Ref3], hence we borrowed the frameworks of ML PES/force field models in this project. In this project we will focus on neural network (NN) and Gaussian process regression (GPR) models.

### Molecular Structural Descriptors
The first problem of designing such ML models is to find appropriate quantities to describe the molecular structures of the cluster systems, which are called descriptors. The raw atomic coordinates are not wise choices, since they are lack of translational, rotational and element permutational invariance, which makes the training of the ML models very inefficient. Like peopel did in building classical force fields, a set of natural candidates of molecular structural descriptors are internal coordinates, including bond lengths, bond angles, torsion angles, etc. Internal coordinates are efficient in building ML PES/force field models for small molecular systems. However, the number of internal coordinates increase rapidly as the size of the system grows. In addition, redundancy also gives difficulties in the training of the ML models.
Researchers have already proposed many types of molecular structural descriptors [^Ref4]. For the easiness of implementation, we choose atomic-centered symmetry functions (ACSF) [^Ref5] [^Ref6] [^Ref7] as the descriptors in our ML models. We have developed Python scripts to evaluate such ACSFs in our studied water clusters (see the notebook https://github.com/QCUncertainty/WaterCluster/blob/main/scripts/ACSF-t1.ipynb). There are several parameters to define such ACSFs, and currently those parameters are not optimized for the water clusters. The ACSF parameters should be optimized and their performance in our models should be evaluated carefully.

### Neural Network (NN) Models
Our NN model is similar to the one in [^Ref5] [^Ref6]. We want to note that this type of NN models are **NOT** typical feed-forward neural networks. Suppose the fitting target is the MBE energy of the system truncated at some order, the MBE energy is decomposed into atomic contributions. Each atom in the cluster system contributes to the total MBE energy, and the sum of these atomic contributions makes the total MBE energy. Only the atomic contributions are described by typical feed-forward neural networks. Atoms of the same element in the system share the same atomic NN (same weights and biases). Of course, the inputs to the atomic NN of differnt atoms are different.

We have developed Python scripts to train the NN model using the Pytoch package (please see https://github.com/QCUncertainty/WaterCluster/blob/main/scripts/MBE-ACSF.ipynb). The training process do not converge straightforwardly. Usually changing the learning rate adaptively is necessary to obtain a good fit.

Models for MBE energies truncated at different orders can be trained by transfer learning. For example, in order to fit the NN model to MBE energy truncated at order 3, one can read in the parameters from the trained NN model for MBE energy truncated at order 2. Usually this transfer learning trick saves a lot of training time.

In order to obtain NN models to predict the uncertainty of MBE energies, we adopt the idea in the article at https://medium.com/@steve_thorn/predicting-uncertainty-with-neural-networks-aec0217eb37d: the variance of each MBE energy prediction is calcualted and then a new NN model is trained to fit these variances. 

Until now, we found the NN model fitted to the structures of source 1 above did not give good predictions for the structures of source 2. This is not a surprise, since in the structures of source 1 only a very small portion represent local minimums on the PES. We have to extend our training set if we want our NN model to describle low-lying energy structures well.


### Gaussian Process Regression (GPR) Models
GPR is a powerful and flexible regression technique used in statistics and machine learning. In a GPR model, the to-be-fitted variable is described by a random function of the input variables, and any finite collection of the function values obey a multivariate normal (Gaussian) distribution. This random function forms a Gaussian process, a type of stochastic process [^Ref8]. The goal of building a GPR model is to find the corresponding random function values with the largest probabilities given certain inputs. One of the advantage of GPR models is that at the same time as a prediction is made, the corresponding error of this prediction (variance) is also obtained, since we assume the predictions (function values) obey a Gaussian distribution. Other ML models such as NN models do not have this feature, hence the error of the model prediction should be trained and predicted separately (for example, the NN model above). The key quantity to characterize a GPR model is the covariance (kernel) function, which measures how similar the input data points are to one another in Gaussian processes. The parameters of the chosen covariance function can be optimzed by maximizing the likelihood of the data.

We follow the design in the publication [^Ref9], in which a GPR model for interatomic potential is proposed (Gaussian approximation potential, GAP). Similar to the NN model above, the total MBE energy is decomposed into atomic contributions and each atomic contribution is described by a sub model. The GAP code is available in the package of [QUIP](https://github.com/libAtoms/QUIP), and the documentation is available [here](https://libatoms.github.io/GAP/).

Currently there are still difficulties hindering the running of the GAP code (official examples do not run on our local machine). Our plan is to modify the GAP code to use ACSFs as inputs, and then predict the MBE energies as well as their uncertainty.


[^Ref1]: Avijit Rakshit and Pradipta Bandyopadhyay, Joseph P. Heindel and Sotiris S. Xantheas, “Atlas of putative minima and low-lying energy networks of water clusters n=3-25”, *J. Chem. Phys.* **151**, 214307 (2019).

[^Ref2]: Jörg Behler, "Four Generations of High-Dimensional Neural Network Potentials", *Chem. Rev.* **121**, 10037 (2021).

[^Ref3]: Oliver T. Unke, Stefan Chmiela, Huziel E. Sauceda, Michael Gastegger, Igor Poltavsky, Kristof T. Schütt, Alexandre Tkatchenko, and Klaus-Robert Müller, "Machine Learning Force Fields", *Chem. Rev.* **121**, 10142 (2021).

[^Ref4]: Felix Musil, Andrea Grisaﬁ, Albert P. Bartók, Christoph Ortner, Gábor Csányi, and Michele Ceriotti, "Physics-Inspired Structural Representations for Molecules and Materials", *Chem. Rev.* **121**, 9759 (2021).

[^Ref5]: Jörg Behler and Michele Parrinello, "Generalized Neural-Network Representation of High-Dimensional Potential-Energy Surfaces", *Phys. Rev. Lett.* **98**, 146401 (2007).

[^Ref6]: Jörg Behler, "Atom-centered symmetry functions for constructing high-dimensional neural network potentials", *J. Chem. Phys.* **134**, 074106 (2011).

[^Ref7]: Alea Miako Tokita and Jörg Behler, "How to train a neural network potential", *J. Chem. Phys.* **159**, 121501 (2023).

[^Ref8]: Emanuel Parzen, "Stochastic Processes", Courier Dover Publications (2015).

[^Ref9]: Albert P. Bartók, Mike C. Payne, Risi Kondor, and Gábor Csányi, "Gaussian Approximation Potentials: The Accuracy of Quantum Mechanics, without the Electrons", *Phys. Rev. Lett.* **104**, 136403 (2010).
 