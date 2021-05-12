import os
import glob
from setuptools import setup, find_packages

setup(
    name = 'DeNoPro',
    version = 0.1,
    author = 'MSCTR',
    entry_points = {
        'console_scripts': ['denopro = lib.launcher:launch']
    },
    description = "Denovo Proteogenomics Pipeline to identify clinically relevant novel variants from RNAseq and Proteomics data.",
    url = 'https://github.com/MSCTR/Denovo-Proteogenomics-Pipeline',
    packages = find_packages()
)

