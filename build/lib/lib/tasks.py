from denoprolib import trinity

from configparser import ConfigParser
import argparse
import sys
import os
import pathlib 

class configReader():
    base_parser = argparse.ArgumentParser(add_help=False,
                                          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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
    
class Assemble(configReader):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="Denovo assembly of RNAseq reads",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser.add_argument('--cpu', help="Maximum number of threads to be used by Trinity",
                                default = '30')
            parser.add_argument('--max_mem', help="Maximum amount of RAM (in Gs) that can be allocated",
                                default='50G')

            args = parser.parse_args(sys.argv[2:])

            self.cpu = args.cpu
            self.max_mem = args.max_mem
            config_file = args.config_file
        
        else:
            self.cpu = kwargs.get('cpu')
            self.max_mem = kwargs.get('max_mem')
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)

        if self.config.has_option('directory_locations', 'output_dir'):
            self.output_dir = pathlib.PurePath(self.config.get('directory_locations', 'output_dir'), 'Trinity')
        else:
            print("Please specify an output directory")
    
    def run(self):
        path = configReader.get_fastq(self)
        trinity.nonEmpty(path, self.cpu, self.max_mem, self.output_dir)

class SearchGUI_Peptideshaker(configReader):
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
        path = configReader.get_spectra(self)
        os.system(f"Rscript denoprolib/Searchgui_peptideshaker_edit.R {path}")

class novel_peptide(configReader):
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
        os.system(f"Rscript denoprolib/novel_peptide_identification_edit.R {self.dir}")
