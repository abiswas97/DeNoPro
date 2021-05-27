import configparser
import PySimpleGUI as sg
import subprocess
import sys
from os import path
from configparser import ConfigParser


CONFIG_FILE = path.join(path.dirname(__file__), r"test.conf")
parser = ConfigParser()
parser.optionxform = str
parser.read(CONFIG_FILE)

# this dict will be updated and then saved to original conf file
conf_keys = {
    'output_dir': ['directory_locations','','-OUTDIR-'],
    'fastq_for_trinity': ['directory_locations','','-FASTQ-'],
    'spectra_files': ['directory_locations','','-SPECTRA-'],
    'trinity': ['dependency_locations','','-TRINITY-'],
    'hg19': ['dependency_locations','','-HG19-'],
    'searchgui': ['dependency_locations','','-SEARCHGUI-'],
    'peptideshaker': ['dependency_locations','','-PEPTIDE-'],
    'denopro_path': ['denopro_location','','-DENOPRO-'],
    'theme': ['gui_settings','','-THEME-']
    }

default_conf = {
    'directory_locations': ['output_dir', 'fastq_for_trinity', 'spectra_files'],
    'dependency_locations': ['trinity', 'hg19', 'searchgui', 'peptideshaker'],
    'denopro_location': ['denopro_path'],
    'gui_settings': ['theme']
    }

############################################################    
#                     Functions
############################################################
def runCommand(cmd, timeout=None, window=None):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.refresh() if window else None
    
#    retval = p.wait(timeout)
#    return (retval,output)
    return output

def load_parser(config_file):
    parser = ConfigParser()
    parser.optionxform = str
    try:
        parser.read(config_file)
    except Exception as e:
        sg.popup(f'Exception {e}', 'No config file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
    return parser

def save_config(config_file,parser,values):
    if values:
        for k,v in conf_keys.items():
            try:
                if parser.has_section(v[0]):
                    if parser.has_option(v[0], k):
                        parser.set(v[0],k,values[v[2]])
            except Exception as e:
                print(f'Problem updating config from window values. Key = {k}')

    with open(config_file, 'w') as conf_file:
        parser.write(conf_file)
    
    sg.popup('Configuration saved!')

def create_parser():
#    new_path = path.join(path.dirname(__file__), r"new_config.conf") 
    new_parser = configparser.ConfigParser()
    for k,v in default_conf.items():
        new_parser.add_section(k)
        for value in v:
            new_parser.set(k,v,value)
    return new_parser    

############################################################    
#             Creating Configuration Window
############################################################

def create_conf_window(parser):
    sg.theme(parser.get('gui_settings','theme'))

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(25,1))

    layout = [
        [sg.Text('Choose Configuration', font = 'Helvetica 20', justification='c')],
        [sg.HSeparator()],
        [TextLabel('Output Directory'), sg.Input(key='-OUTDIR-'), sg.FolderBrowse(target='-OUTDIR-')],
        [TextLabel('FASTQ Files Directory'), sg.Input(key='-FASTQ-'), sg.FolderBrowse(target='-FASTQ-')],
        [TextLabel('Spectra Files Directory'), sg.Input(key='-SPECTRA-'), sg.FolderBrowse(target='-SPECTRA-')],
        [TextLabel('Hg19 Reference'), sg.Input(key='-HG19-'), sg.FileBrowse(target='-HG19-')],
        [TextLabel('SearchGUI'), sg.Input(key='-SEARCHGUI-'), sg.FileBrowse(target='-SEARCHGUI-')],
        [TextLabel('PeptideShaker'), sg.Input(key='-PEPTIDE-'), sg.FileBrowse(target='-PEPTIDE-')],
        [TextLabel('Path to Trinity'), sg.Input(key='-TRINITY-'), sg.FileBrowse(target='-TRINITY-')],
        [TextLabel('Path to DeNoPro directory'), sg.Input(key='-DENOPRO-'), sg.FolderBrowse(target='-DENOPRO-')],
        [TextLabel('Theme'), sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
        [sg.Text('')],
        [sg.Text('')],
#        [sg.HSeparator()],
#        [TextLabel('Save As'), sg.Input(key = '-NEW_CONF-'), sg.FileBrowse(target='-NEW_CONF-')],
        [sg.Button('Save'), sg.Button('Exit')]
    ]
    window = sg.Window("Config", layout, keep_on_top=True, finalize=True)

    for k,v in conf_keys.items():
        try:
            window[conf_keys[k][2]].update(value=parser.get(v[0],k))
        except Exception as e:
            print(f'Problem updating GUI window from config. Key = {k}')
    return window

############################################################    
#              Main Program and Event Loop 
############################################################
def main():
    main_window, parser = None, load_parser(CONFIG_FILE)

    command_to_run = 'denopro '
    layout = [
        [sg.Text('DeNoPro : de novo Proteogenomics Pipeline', font='Helvetica 20', justification='c')],
        [sg.Text('')],
        [sg.Text('Mode', size=(6,1), justification='r'), sg.Combo(['assemble','customdb','findnovel','survival','novelorf'],key='mode'),sg.Text('CPU:', size=(6,1), justification='r'), sg.Input(size=(3,1), key='cpu'), sg.Text('Max mem:', size=(9,1), justification='r'), sg.Input(size=(3,1), key='max_mem')],
        [sg.Text('Config', size=(6,1), justification='r'), sg.Input(key='-config-'),sg.FileBrowse('Select', target='-config-')],
        [sg.Text('')],
        #output
        [sg.Text('Final Command:')], 
        [sg.Text(size=(70,5),key='command_line', text_color='yellow',font='Courier 10')],
        [sg.MLine(size=(90,20), reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, write_only=True, font='Courier 10', autoscroll=True, key='-ML-')],
        [sg.Button("Start"), sg.Button('Exit'), sg.Button('Change Configuration')]
    ]   

    main_window = sg.Window('DeNoGUI', layout, finalize=True)

    while True: 
        event,values = main_window.read()
        # define exit
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # Config Loop
        if event == 'Change Configuration':
            # set the main config (if called)
            event,values = create_conf_window(parser).read(close=True)
            if event == 'Save':
                save_config(CONFIG_FILE,parser,values)
        # Main Loop
        if event == 'Start':
            params = ''
            params += f"{values['mode']} -c {values['config']} --cpu {values['cpu']} --max_mem {values['max_mem']}G"
            command = command_to_run + params
            main_window['command_line'].update(command)
            runCommand(cmd = command, window=main_window)
        
    main_window.close()

if __name__ == '__main__':
    sg.theme('DarkGrey13')
    main()
