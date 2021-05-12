import argparse
import sys

def launch():
    parser = argparse.ArgumentParser(
        description = 'DeNoPro: Denovo Proteogenomics Pipeline to identify clinically relevant novel variants from RNAseq and Proteomics data',
        usage = """ denopro <mode> [<args>]

        Modes are:

        - assemble:  denovo assembly of transcript sequences using Trinity
        - customdb:  produces custom peptide database from assembled transcripts 
                     which are mapped against proteomics data
        - findnovel: maps potential novel peptides from customdb to a reference 
                     tracriptome, outputting a list of confident novel peptides
        - survival: 
        - novelorf: 

        denopro <mode> -h for specific help
        """)
    parser.add_argument('mode', metavar = "<MODE>", help = 'denopro mode (assemble, customdb, findnovel, survival or novelorf)',
                        choices = ['assemble', 'customdb', 'findnovel', 'survival', 'novelorf'])
    args = parser.parse_args(sys.argv[1:2])

    tasks = {
        'assemble': Assemble,
        'customdb': SearchGUI_Peptideshaker,
        'findnovel': Novel_peptide_identification,
        'survival': Survival_analysis,
        'novelorf': Potential_novel_orf
    }

    if args.node not in tasks:
        print("Unsupported mode")
        parser.print_help()
        exit(1)
    
    Task = tasks[args.mode]
    Task().run()
