# Running Many-body Expansion Calculations with QCArchive/QCManyBody on A Local Machine

This document explains how to set up a QCArchive data server (QCFractal), a computational manager and computational workers (QCFractalCompute), and run high throughput many-body expansion calculations with QCManybody on a local machine. Usually this type of calculations are done on computer clusters or supercomputers, which will be documented elsewhere. However, the full control of a local machine facilitates testing and debugging. The purpose of this document is to illustrate the full workflow of such calculations. 

## Basics of QCArchive and QCManybody
[QCArchive](https://molssi.github.io/QCFractal/index.html) is a platform developed by [the Molecular Sciences Software Institue (MolSSI)](https://molssi.org/) for running high throughput quantum chemistry calculations. Many popular quantum chemistry packages such as Psi4, NWChem, etc, can be supported through [QCEngine](https://github.com/MolSSI/QCEngine). QCArchive has [multiple components](https://github.com/MolSSI/QCFractal), such as a data server (QCFractal), client interface (QCPortal) and computational workers (QCFractalCompute). A data server to store and manage the calculation results, computational nodes (called workders) doing the actual calculations, and a computational manager to manage all workers must be run before any calculation can be done. In practical calculations, users create clients and talk to the data server through QCPortal, add calculation specifications (settings) and submit the calculations to the computational manager. The manager then asign the computational jobs to the workders and also mornitor these jobs. Users can check the status of the jobs. When the jobs are done, the calculation results are stored in the database managed by the data server. Users can access and handle the data through the data API. A tutorial of QCArchive and demo jupyter notebooks can be found [here](https://github.com/MolSSI/QCArchiveDemos/blob/main/qcarchive_workshop.ipynb).
[QCManybody](https://github.com/MolSSI/QCManyBody) is a python package for many-body expansion calculations on molecular clusters. It is independent from the quantum chemistry engine it uses. Its documentation (incomplete) can be found [here](https://molssi.github.io/QCManyBody/).

## Set Up A QCFractal Data Server
The QCFractal server uses [PostgreSQL](https://www.postgresql.org/) to store the data in a database. First, a python environment should be created and activated in order to run a QCFractal server. If conda is used as the python package manager, the corresponding commands are:
```
conda create -n qcf_server qcfractal postgresql -c conda-forge
conda activate qcf_server
```
Once the environment is ready, one can create a directory to hold all QCFractal server files and initialize an example configuration file in the directory with the commands
```
mkdir qcf_server
qcfractal-server --config=qcf_server/qcf_config.yaml init-config
```
An example configuration file may look like
```
name: QCFractal Server # user-specified name of the server
enable_security: false # disable user password or not
allow_unauthenticated_read: true # allow user to check data without login or not
hide_internal_errors: False
logfile: qcfractal_server.log # user-specified name of the log file. If not set logging to the console
loglevel: DEBUG # control how much info should be logged
statistics_frequency: 3600 
service_frequency: 60
max_active_services: 20
heartbeat_frequency: 1800
log_access: false
database:
  base_folder: qcf_server
  host: localhost
  port: 5432
  database_name: qcfractal_default
  own: true
api:
  host: 127.0.0.1 # ip address for the local machine
  port: 7777 # port for access. In this case the
  secret_key: vLzQuQ5lXz_Je85ck9oiwSribN58LDRMAukmLvpaYX4
  jwt_secret_key: GrCkZz6mUhu8rm2E3tZD4OEMuO8wHblLHlGRaqnfSVI
```
Users can modify the configuration file according to their needs.
After the configuration file is created, one can initialize the database by running
```
qcfractal-server --config=qcf_server/qcf_config.yaml init-db
```
One then can see a directory ```postgres``` is created under ```qcf_server```. If for some reason the database needs to be cleaned, one can remove the directory ```postgres``` and re-run the database initialization command above.
The configuration info can be checked by the command
```
qcfractal-server --config=qcf_server/qcf_config.yaml info
```
If everything looks fine, the data server can be started by the command
```
qcfractal-server --config=qcf_server/qcf_config.yaml start
```
The server can be stopped by applying **Ctrl+C** to the server start run.
## Set Up A QCFractal Computation Manager and Workers
A special python environment should be created and activated to run a QCFractal computational manager. The conda commands are
```
conda create -n qcfractal-new_mb
conda activate qcfractal-new_mb
```
In order to support QCManyBody, this environment should be built from the ```new_mb``` branch of QCFractal. So one has to clone the branch first by running
```
git clone -b new_wb https://github.com/MolSSI/QCFractal.git
```
Inside the ```qcfractal-new_mb``` environment, quantum chemistry engines like psi4 can be installed:
```
conda install psi4
```
Then pip installations of QCPortal, QCFractal, QCFractalCompute, QCArchiveTesting and QCManyBody should be run:
```
pip install ./qcportal ./qcfractal ./qcfractalcompute ./qcarchivetesting
pip install "qcmanybody@git+https://github.com/MolSSI/QCManyBody"
```
In addition, another python enviroment for the workders should be created by the command
```
conda env create -f worker-env.yml
```
in which the environment file ```worker-env.yml``` reads
```
# worker-env.yml

name: qcfractal-worker-psi4 # user-specified name of the environment
channels:
  - conda-forge/label/libint_dev
  - conda-forge
  - defaults
dependencies:
  - python =3.12 # this version no. depends on the user's python installation
  - pip
  - qcengine
  - psi4 # suppose psi4 is used as the quantum chemistry engine
  - nwchem # optional, nwchem can also be used
  - dftd3-python # optional, DFT-D3 is used for dispersion correction
  - gcp-correction
  - geometric
  - scipy

  - pip:
    - basis_set_exchange # for basis set choices
```
A manager configuration file ```qcfractal-manager-config.yml``` should also be created. An example is shown below:
```
# qcfractal-manager-config.yml

cluster: single_workstation           # descriptive name to present to QCFractal server
loglevel: DEBUG
logfile: qcfractal-manager.log
update_frequency: 30.0

server:
  fractal_uri: http://127.0.0.1:7777      # server url 
  username: null # for simplicity no username/password are required
  password: null
  verify: False

executors:
  test_local:
    type: local 
    max_workers: 1           # max number of workers
    cores_per_worker: 2          # cores per worker
    memory_per_worker: 2         # memory per worker, in GiB
    queue_tags:                   # only claim tasks with these tags; '*' means all tags accepted
      - '*'
    environments:
      use_manager_environment: True   # use the manager environment for task execution, not recommended
      conda:
        - qcfractal-worker-psi4    # user-specified name of conda env used for task execution
    worker_init:
      - source /home/yzhang/Work/AmesLab/LDRD/QCFractal/worker-init.sh   # initialization script for the workers with the user-specified path
```
For computer clusters or supercomputers, job schedulers like lsf can be chosen and the corresponding queue parameters can be set. A slightly different example ```qcfractal-manager-config.yml``` file can be found [here](https://molssi.github.io/QCFractal/admin_guide/managers/index.html#compute-manager-local). 
An example worker initialization script ```worker-init.sh```reads
```
# worker-init.sh
#!/bin/bash

# Make sure to run bashrc
source $HOME/.bashrc

# Don't limit stack size
ulimit -s unlimited

# make scratch space
# CUSTOMIZE FOR YOUR CLUSTER
mkdir -p /tmp/${USER}/${LSB_JOBID}
cd /tmp/${USER}/${LSB_JOBID}

# Activate qcfractalcompute conda env
conda activate qcfractal-new_mb
```
When all the files above are ready, the computational manager can be started using the command
```
qcfractal-compute-manager --verbose --config config.yml
```
Similar to the data server, the computational manager and workders can be stopped by **Ctrl+C**.
When all the steps above are properly done, the data server and computational manager are ready for accepting computational jobs.

## Create A Singlepoint Energy Calculation Dataset with QCArchive
In the currentl implementation of QCManyBody, the full-body system energy is not available if the many-body expansion is truncated at a order lower than the total no. of the monomers of the system, which is unavoidable for large molecular clusters such as 30-mer systems. So in order to calculate the errors of the truncated many-body expansions, a separated singlepoint energy of the full-body systems should be done. The jupyter notebook ```sp_dataset.ipynb``` under ```scripts/``` in this repository is for this purpose.

In order to run the notebook, one needs a stacked xyz file containing all the geometries of the molecular clusters. One example file of water trimers reads
```
9
substructure 3-mer 8 from 6-mer
O 25.9126797 4.29365396 27.7117825
H 26.4442463 4.54399681 26.9467773
H 25.2130337 3.73617911 27.3463573
O 24.1495838 5.72118950 25.2537212
H 24.1281662 6.19553995 26.0985832
H 23.8597832 4.82338667 25.4574318
O 26.1187897 2.45435238 24.4402142
H 26.8724747 1.88090622 24.3252258
H 26.4757614 3.35144091 24.5405731
9
substructure 3-mer 9 from 6-mer
O 25.9126797 4.29365396 27.7117825
H 26.4442463 4.54399681 26.9467773
H 25.2130337 3.73617911 27.3463573
O 24.1495838 5.72118950 25.2537212
H 24.1281662 6.19553995 26.0985832
H 23.8597832 4.82338667 25.4574318
O 23.9541073 2.93191457 26.0668354
H 24.6537933 2.63791275 25.4587955
H 23.2909279 2.24694753 26.0709209
9
substructure 3-mer 10 from 6-mer
O 25.9126797 4.29365396 27.7117825
H 26.4442463 4.54399681 26.9467773
H 25.2130337 3.73617911 27.3463573
O 26.1187897 2.45435238 24.4402142
H 26.8724747 1.88090622 24.3252258
H 26.4757614 3.35144091 24.5405731
O 23.9541073 2.93191457 26.0668354
H 24.6537933 2.63791275 25.4587955
H 23.2909279 2.24694753 26.0709209
```
The script will read these water trimer geometries in one by one, and add delimiters to separate fragments, such as
```
O 25.9126797 4.29365396 27.7117825
H 26.4442463 4.54399681 26.9467773
H 25.2130337 3.73617911 27.3463573
--
O 24.1495838 5.72118950 25.2537212
H 24.1281662 6.19553995 26.0985832
H 23.8597832 4.82338667 25.4574318
--
O 26.1187897 2.45435238 24.4402142
H 26.8724747 1.88090622 24.3252258
H 26.4757614 3.35144091 24.5405731
```
A singlepoint energy QCArchive dataset (called ```ds``` here) can be created through the following function:
```
ds = client.add_dataset("singlepoint",
                        name=DATASET_NAME,
                        description=DATASET_DESCRIPTION)
```
The calculation specification can be set in the following dictionary:
```
sp_spec = {
    "program": "psi4",
    "driver": "energy",
    "method": "b3lyp",
    "basis": "6-31G*",
    "keywords": {"e_convergence": 1e-10, "d_convergence": 1e-10},
}
```
The water trimers are added as entries into the dataset with the specification above. Finally the dataset (a bundle of calculations) is submitted to the computational manager through the function ```ds.submit()```. The status of the dataset can be checked through ```ds.print_status()```. Once all the calculations are done, the results ("records") can be shown with the lines
```
rec = ds.get_record('trimer_0', 'b3lyp/6-31G*')
print(rec.properties['return_energy'])
```

## Create A Many-Body Expansion Calculation Dataset with QCArchive/QCManyBody
Creating a many-body expansion calculation dataset is similar to creating a singlepoint energy calculation dataset. This can be done through the notebook ```scripts/mbe_dataset.ipynb``` in the repository. However, the package QCManyBody should be imported and used:
```
from qcportal.manybody import ManybodySpecification
```
For example, the many-body expansion calculation can be specified in the following way:
```
sp_spec = {
    "program": "psi4",
    "driver": "energy",
    "method": "b3lyp",
    "basis": "6-31G*",
    "keywords": {"e_convergence": 1e-10, "d_convergence": 1e-10},
}

mb_spec = ManybodySpecification(
    bsse_correction=['vmfc'],
    levels={1: sp_spec, 2: sp_spec, 3: sp_spec},
)
```
Here, the "vmfc" approach is used for BSSE correction, and we asign the same specification to all orders (1-3) of calculations. No truncation applies here. A many-body expansion dataset (called "ds_w3_mbe" here) can be created through the following function:
```
ds_w3_mbe = client.add_dataset("manybody", name=DATASET_NAME description=DATASET_DESCRIPTION)
```
Adding entries and specifications, submitting, checking status and showing results of this dataset is similar to those of a singlepoint energy calculation dataset.
                    