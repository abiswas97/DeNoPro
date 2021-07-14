# DeNoPro

DeNoPro - a denovo proteogeomics pipeline to identify clinically relevent novel variants from RNAseq and Proteomics data.

## Contents ##
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)

## Introduction
DeNoPro provides a pipeline for the identification of novel peptides from matched RNAseq and MS/MS proteomics data. 

The pipeline consists of de novo transcript assembly (Trinity), generation of a protein sequence database of 6-frame translated transcripts, and a combination of search engines (X! Tandem, MS-GF+, Tide) to query the custom database. Identified novel peptides and protein variants are then filtered by confidence and mapped to gene models using ACTG.  


## Installation
To install DeNoPro as a python module, open a terminal in the directory containing setup.py, and run
```
python setup.py install
```
DeNoPro can be made executable by running `chmod u+x denopro`.

## Dependencies

DeNoPro has been tested with Python 3, Python 2 is not supported at this time. R version 4.0.0 or greater is required to run the PGA package. 

We recommend using a conda environment to maintain dependencies, and an environment config file using Python 3.9.6 and R 4.0.5 has been provided. To setup the conda environment, run `conda env create -f denopro-env.yml` and activate with `conda activate denopro-env`.

### Required software

#### Included in conda environment
1. [Trinity](https://github.com/trinityrnaseq/trinityrnaseq/wiki) version 2.8.5
    
    Used during `assemble` for de novo assembly of RNA transcripts 

2. [PGA](https://github.com/wenbostar/PGA) (R>4.0)
    
    Used in `customdb` for creation of 6-frame translated protein database 

3. [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
    
    Used to run the GUI functionality

#### Not included in conda environment
1. [SearchGUI](https://compomics.github.io/projects/searchgui) version [3.3.17](https://mvnrepository.com/artifact/eu.isas.searchgui/SearchGUI/3.3.17)
    
    Uses the `X! Tandem`, `MS_GF+` and `Tide` search engines to search created custom database against mgf spectra files

2. [PeptideShaker](https://compomics.github.io/projects/peptide-shaker) version [1.16.42](https://mvnrepository.com/artifact/eu.isas.peptideshaker/PeptideShaker/1.16.42)
    
    Used to select matching identifications among the three search engines to output a list of confident novel peptides and their corresponding proteins

3. [ACTG](https://academic.oup.com/bioinformatics/article/33/8/1218/2748210)
    
    Used to map identified confident novel peptides to their corresponding genomic locations

4. [Bamstats](https://github.com/guigolab/bamstats)
    
    Used to process expression levels of novel peptides 

## Usage

DeNoPro was designed to be modular, to account for large processing times. The modes are

`assemble` : de novo assembly of transcript sequences using Trinity

`searchdb` : produces custom peptide database from assembled transcripts which are mapped against proteomics data

`identify` : maps potential novel peptides from searchdb to a reference tracriptome outputting a list of confident novel peptides

`novelorf` : finds novel ORFs in identified novel peptides

`quantify` : evaluates expression levels of identified novel peptides in a sample

The standard workflow is 
    `assemble` >> `searchdb` >> `identify` >> `novelorf` >> `quantify`

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
