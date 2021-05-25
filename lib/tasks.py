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
    
    def output_dir(self):
        if self.config.has_option('directory_locations', 'output_dir'):
            output_dir = self.config.get('directory_locations', 'output_dir')
        else:
            print("Please specify an output directory in the configuration file.")
        return output_dir
    
    def trinity_output_dir(self):
        if self.config.has_option('directory_locations', 'output_dir'):
            trinity_output_dir = pathlib.PurePath(self.config.get('directory_locations', 'output_dir'), 'Trinity')
        else:
            print("Please specify an output directory in the configuration file.")
        return trinity_output_dir

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
    

class assemble(configReader):
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

        self.output = self.trinity_output_dir()

        if self.config.has_option('directory_locations', 'fastq_for_trinity'):
            self.fastq = self.config.get('directory_locations', 'fastq_for_trinity')
        else:
            print("Please specify a directory containing FASTQ files")
        
        if self.config.has_option('dependency_locations', 'trinity'):
            self.trinity_path = self.config.get('dependency_locations', 'trinity')
        else:
            self.trinity_path = 'Trinity'

    def run(self):
        trinity.runTrinity(self.trinity_path, self.fastq, self.cpu, self.max_mem, self.output)

class searchguiPeptideshaker(configReader):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="Custom peptide database from assembled transcripts",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            args = parser.parse_args(sys.argv[2:])

            config_file = args.config_file
        
        else:
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)

        self.trinity_out = self.trinity_output_dir()
        self.searchgui = self.config.get('dependency_locations', 'searchgui')
        self.peptideshaker = self.config.get('dependency_locations', 'peptideshaker')
        self.hg19 = self.config.get('dependency_locations', 'hg19')
        self.output = self.output_dir()

        if self.config.has_option('directory_locations', 'spectra_files'):
            self.spectra = self.config.get('directory_locations', 'spectra_files')
        else:
            print("Please specify a directory containing MS/MS spectra files")

    def run(self):
        os.system(f"Rscript denoprolib/Searchgui_peptideshaker_edit.R {self.spectra} {self.trinity_out} {self.searchgui} {self.peptideshaker} {self.hg19} {self.output}")

class novelPeptide(configReader):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="identify confident novel peptides",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            
            args = parser.parse_args(sys.argv[2:])

            config_file = args.config_file
        else:
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)
        self.output = self.output_dir()
    
        if self.config.has_option('dependency_locations', 'actg'):
            self.actg = self.config.get('dependency_locations', 'actg')
        else:
            print("Please specify the directory containing ACTG")

    def run(self):
        os.system(f"Rscript denoprolib/novel_peptide_identification_edit.R {self.output} {self.actg}")

class survivalAnalysis(configReader):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="Survival Analysis",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            
            args = parser.parse_args(sys.argv[2:])

            config_file = args.config_file
        else:
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)
        self.output = self.output_dir()
    
    def run(self):
        os.system(f"Rscript denoprolib/Survival_analysis_novel_peptides.R {self.output}")

class potentialNovelORF(configReader):
    def __init__(self, **kwargs):
        if not kwargs:
            parser = argparse.ArgumentParser(
                description="Identify potential novel ORFsz",
                parents=[self.base_parser],
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            
            args = parser.parse_args(sys.argv[2:])

            config_file = args.config_file
        else:
            config_file = kwargs.get('config_file')
        
        self.config = self.read_config(config_file)
        self.output = self.output_dir()
    
    def run(self):
        os.system(f"sh denoprolib/Potential_novel_ORF.sh {self.output}")



