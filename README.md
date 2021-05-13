# DeNoPro

DeNoPro - a denovo proteogeomics pipeline to identify clinically relevent novel variants from RNAseq and Proteomics data.

## Contents ##
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)

## Introduction
DeNoPro provides a pipeline for the identification of novel peptides from matched RNAseq and MS/MS proteomics data. 

Paired or singled end reads are first assembled using Trinity and six-frame translated. This output is used to create a custom peptide database using SearchGUI, which can then be mapped against proteomics data. 

## Installation
To install DeNoPro as a python module, open a terminal in the directory containing setup.py, and run
```
python setup.py install
```

## Usage

### Assemble 
denovo assembly of transcript sequences using Trinity
#### Usage

### CustomDB 
Produces custom peptide database from assembled transcripts which are mapped against proteomics spectra


### FindNovel 
Maps potential novel peptides from customdb to a reference tracriptome, outputting a list of confident novel peptides


### Survival


### NovelORF
