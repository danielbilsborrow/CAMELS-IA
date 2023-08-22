#!/bin/bash
#requesting one node
#SBATCH -N1
#requesting 1 core
#SBATCH -n1

#!/bin/bash
#requesting one node
#SBATCH -N1
#requesting 1 core
#SBATCH -n1
#SBATCH --mail-user=zcapdjl@ucl.ac.uk
#SBATCH --mail-type=ALL

cd  /share/data1/zcapdjl/CAMELS-IA/ellipticity_measurements

python3 09a.find_ellipticities.py

