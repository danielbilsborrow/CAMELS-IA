#!/bin/bash
#requesting one node
#SBATCH -N1
#requesting 1 core
#SBATCH -n1

cd  /share/data1/zcapdjl/CAMELS-IA
python downloadLHsim.py

