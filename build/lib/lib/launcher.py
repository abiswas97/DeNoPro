import argparse
import sys
import time
import os

from lib.tasks import assemble, searchguiPeptideshaker, novelPeptide, survivalAnalysis, potentialNovelORF
from lib import denoprogui

class launchGUI(argparse.Action):
    def __call__(self, parser, values, namespace, option_string):
        print("Launching GUI")
        time.sleep(1)
        denoprogui.main()
        parser.exit()

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
    parser.add_argument('-g','--gui', help = 'Launches the GUI functionality',nargs = 0, action=launchGUI)
    args = parser.parse_args(sys.argv[1:3])

    modes = {
        'assemble': assemble,
        'customdb': searchguiPeptideshaker,
        'findnovel': novelPeptide,
        'survival': survivalAnalysis,
        'novelorf': potentialNovelORF
    }

    print(parser.usage)
    time.sleep(2)
 
#    if args.gui:
#        print("Launching GUI")
#        time.sleep(1)
#        os.system('python denoprogui.py')

    if args.mode not in modes:
        print("Unsupported mode")
        parser.print_help()
        exit(1)

    Mode = modes[args.mode]
    Mode().run()

    