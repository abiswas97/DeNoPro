import configparser
import PySimpleGUIQt as sg
import subprocess
import sys
from os import path
from configparser import ConfigParser

sg.theme("SystemDefault")

def TextLabel(text): return sg.Text(text+':', justification='r', size=(25,1)) 

frame1= [
    [TextLabel('Output Directory'), sg.Input(key='-OUTDIR-'), sg.FolderBrowse(target='-OUTDIR-')],
    [TextLabel('FASTQ Files Directory'), sg.Input(key='-FASTQ-'), sg.FolderBrowse(target='-FASTQ-')],
    [TextLabel('Spectra Files Directory'), sg.Input(key='-SPECTRA-'), sg.FolderBrowse(target='-SPECTRA-')]
]
frame2= [
    [TextLabel('Trinity'), sg.Input(key='-TRINITY-'), sg.FileBrowse(target='-TRINITY-')],
    [TextLabel('hg19'), sg.Input(key='-HG19-'), sg.FileBrowse(target='-HG19-')],
    [TextLabel('SearchGUI'), sg.Input(key='-SEARCHGUI-'), sg.FileBrowse(target='-SEARCHGUI-')],
    [TextLabel('PeptideShaker'), sg.Input(key='-PEPTIDE-'), sg.FileBrowse(target='-PEPTIDE-')],
    [TextLabel('ACTG'), sg.Input(key='-ACTG-'), sg.FolderBrowse(target='-ACTG-')]
]
frame3= [
    [TextLabel('Transcriptome GTF'), sg.Input(key='-GTF'), sg.FolderBrowse(target='-GTF-')],
    [TextLabel('Mapping Method'), sg.Combo(['PV','PS','VO','SO'],key='-MAP-')],
    [TextLabel('Protein Database'), sg.Input(key='-DB-'), sg.FileBrowse(target='-DB-')],
    [TextLabel('Serialization File'), sg.Input(key='-SER-'), sg.FileBrowse(target='-SER-')]
]
frame4= [
    [TextLabel('Bamstats'), sg.Input(key='-BAMSTATS'), sg.FileBrowse(target='-BAMSTATS-')],
    [TextLabel('BAM Files'), sg.Input(key='-BAM-'), sg.FolderBrowse(target='-BAM-')],
    [TextLabel('BED File'), sg.Input(key='-BED-'), sg.FileBrowse(target='-BED-')]
]
frame5= [
    [TextLabel('DeNoPro Location'), sg.Input(key='-DENOPRO'), sg.FolderBrowse(target='-DENOPRO-')]
]

layout = [
    [sg.Frame('Directory Locations',frame1)],
    [sg.Frame('Dependency Locations', frame2)],
    [sg.Frame('ACTG Options', frame3)],
    [sg.Frame('Quantification Options',frame4)],
    [sg.Frame('Denopro Location',frame5)]
]

window = sg.Window("Config", keep_on_top=True).Layout([[sg.Column(layout,size = (680,720),scrollable=True)]]).Finalize()

while True:
    event,values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()

"""
layout = [
        [sg.Text('Choose Configuration', font = 'Any 20', justification='c')],
        [sg.Text('')],
        [TextLabel('Output Directory'), sg.Input(key='-OUTDIR-'), sg.FolderBrowse(target='-OUTDIR-')],
        [TextLabel('FASTQ Files Directory'), sg.Input(key='-FASTQ-'), sg.FolderBrowse(target='-FASTQ-')],
        [TextLabel('Spectra Files Directory'), sg.Input(key='-SPECTRA-'), sg.FolderBrowse(target='-SPECTRA-')],
        [TextLabel('Hg19 Reference'), sg.Input(key='-HG19-'), sg.FileBrowse(target='-HG19-')],
        [TextLabel('SearchGUI'), sg.Input(key='-SEARCHGUI-'), sg.FileBrowse(target='-SEARCHGUI-')],
        [TextLabel('PeptideShaker'), sg.Input(key='-PEPTIDE-'), sg.FileBrowse(target='-PEPTIDE-')],
        [TextLabel('Path to Trinity'), sg.Input(key='-TRINITY-'), sg.FileBrowse(target='-TRINITY-')],
        [TextLabel('Path to DeNoPro directory'), sg.Input(key='-DENOPRO-'), sg.FolderBrowse(target='-DENOPRO-')],
        [TextLabel('Theme'), sg.Combo(sg.theme_list(), size=(17, 0.8), key='-THEME-')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button('Save'), 
            sg.InputText('', do_not_clear=False, visible=False, key='-filename-',enable_events=True),
            sg.FileSaveAs('Save As'),sg.Button('Exit')]
    ]
    window = sg.Window("Config", layout, keep_on_top=True, finalize=True)
"""