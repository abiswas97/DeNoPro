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
```
denopro assemble [options]
```

#### Options
* `-c/--config_file`: Point to the path of config file to use. Default is `/denopro.conf`

### CustomDB 
Produces custom peptide database from assembled transcripts which are mapped against proteomics spectra

#### Usage
```
denopro customdb [options] <spectra>
```

#### Arguments
* `<spectra>`: Path to directory containing MS/MS spectra files

#### Options
* `-c/--config_file`: Point to the path of config file to use. Default is `/denopro.conf`


### FindNovel 
Maps potential novel peptides from customdb to a reference tracriptome, outputting a list of confident novel peptides

#### Usage
```
denopro findnovel [options] <dir>
```

#### Arguments
* `<dir>`: Path to directory containing CustomDB output

#### Options
* `-c/--config_file`: Point to the path of config file to use. Default is `/denopro.conf`


### Survival


### NovelORF
