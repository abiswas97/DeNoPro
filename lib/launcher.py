import argparse
import sys
import time

from lib.tasks import assemble, searchguiPeptideshaker, novelPeptide, survivalAnalysis, potentialNovelORF

def launch():
    parser = argparse.ArgumentParser(
        description = 'DeNoPro: Denovo Proteogenomics Pipeline to identify clinically relevant novel variants from RNAseq and Proteomics data',
        usage = """ 
        
             # # # # # # # # # # # # # # # # # # # # # # # # # # 
            #    __            _              ___                #
            #   |  \          | \    |       |   \               #
            #   |   \     _   |  |   |   _   |    \   __    _    #
            #   |    \   / \  |  \   |  / \  |    /  /  \  / \   #
            #   |     | | _/  |   |  | |   | |___/  |     |   |  #
            #   |    /   \__/ |   \  |  \_/  |      |      \_/   #
            #   |   /         |    | |       |                   #
            #   |__/          |    \_|       |                   #
            #                                                    #
             # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
                        denopro <mode> [<args>]

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

    modes = {
        'assemble': assemble,
        'customdb': searchguiPeptideshaker,
        'findnovel': novelPeptide,
        'survival': survivalAnalysis,
        'novelorf': potentialNovelORF
    }

    print(parser.usage)
    time.sleep(2)

    if args.mode not in modes:
        print("Unsupported mode")
        parser.print_help()
        exit(1)

    Mode = modes[args.mode]
    Mode().run()
