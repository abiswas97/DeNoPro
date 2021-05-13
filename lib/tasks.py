from denoprolib import trinity

from configparser import ConfigParser, NoOptionError
import argparse
import sys
import os
import subprocess
import glob
import shutil

class denoproTask(object):
    base_parser = argparse.ArgumentParser(add_help=False,
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    base_parser.add_argument('--ncores', '-p', metavar="<CORES>",
                             help='number of processor cores to use', type=int,
                             default=1)
    base_parser.add_argument('--config_file', '-c', metavar="<CONFIG_FILE>",
                             help='config file to use',
                             default=None)
    config = None

    def read_config(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        return config

    def get_denopro_path(self):
        denopro_path = None
        if self.config.has_option('denopro_location', 'denopro_path'):
            path = self.config.get('denopro_location', 'denopro_path')
            if os.path.exists(path):
                denopro_path = path
            else:
                print("Please specify the path to where you originally"
                    " downloaded DeNoPro in the config file.")
        return denopro_path

    def get_fastq(self):
        fastq_path = None
        if self.config.has_option('directory_locations', 'fastq_for_trinity'):
            path = self.config.get('directory_locations', 'fastq_for_trinity')
            if os.path.exists(path):
                fastq_path = path
            else:
                print("Please specify the path to where FASTQ reads"
                    " are stored in the config file.")
        return fastq_path
    
    def get_spectra(self):
        spectra_path = None
        if self.config.has_option('directory_locations', 'spectra_files'):
            path = self.config.get('directory_locations', 'spectra_files')
            if os.path.exists(path):
                spectra_path = path
            else:
                print("Please specify the path to where spectra files"
                    " are stored in the config file.")
        return spectra_path
    
class Assemble(denoproTask):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="Denovo assembly of RNAseq reads",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            args = parser.parse_args(sys.argv[2:])

            config_file = args.config_file
        
        else:
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)
    
    def run(self):
        path = denoproTask.get_fastq(self)
        trinity.nonEmpty(path)

class SearchGUI_Peptideshaker(denoproTask):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="Custom peptide database from assembled transcripts",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser.add_argument('spectra', metavar="<SPECTRA>",
                                help="Directory containing MS/MS spectra files")
            args = parser.parse_args(sys.argv[2:])

            config_file = args.config_file
        
        else:
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)
    
    def run(self):
        path = denoproTask.get_spectra(self)
        os.system(f"Rscript denoprolib/Searchgui_peptideshaker_edit.R {path}")

class Novel_Peptide(denoproTask):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="identify confident novel peptides",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser.add_argument('dir', metavar="<DIR>",
                                help="Directory containing customdb output")
            
            args = parser.parse_args(sys.argv[2:])

            self.dir = args.dir
            config_file = args.config_file
        
        else:
            self.dir = kwargs.get('dir')
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)
    
    def run(self):
        os.system(f"Rscript denoprolib/Novel_peptide_identification_edit.R {self.dir}")
