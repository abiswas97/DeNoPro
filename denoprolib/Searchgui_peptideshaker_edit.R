#!/usr/bin/Rscript
args <- commandArgs(TRUE)

library("PGA")

spectra_files = args[1]
trinity_out = args[2]
searchgui = args[3]
peptideshaker = args[4]
hg19 = args[5]
output = args[6]

setwd(trinity_out)
trinity_output <- list.files(pattern="*Trinity.fasta$")

setwd(output)
#setwd(spectra_files)
#system(find ./ -name '*.mzML' -exec msconvert --filter "peakPicking true 2-" --mgf {} \;)

for (k in 1:length(trinity_output)) {
    i=trinity_output[k]
    outdb <- createProDB4DenovoRNASeq(infa=i,outfile_name =i)
    system(paste("awk 'BEGIN{ RS = \">\"; } { if ($0 !~ /#REV#/) { printf \">\"$0; } }' ",i,"_txFinder.fasta > ",i,"_txFinder_rev_removed1.fasta",sep=''))
    system(paste("awk 'BEGIN{FS=\"|\"}{if(/^>/){print \">\"$2}else{print $0}}' ",i,"_txFinder_rev_removed1.fasta >  ",i,"_txFinder_rev_removed_fasta_trimmed1.fasta",sep=''))
    system(paste("cat ",hg19," ",i,"_txFinder_rev_removed_fasta_trimmed1.fasta > ",i,"_exp_fasta_for_searching.fasta",sep=''))
    system(paste("java -cp ",searchgui," eu.isas.searchgui.cmd.FastaCLI -in ",i,"_exp_fasta_for_searching.fasta -decoy",sep=''))
    system(paste("java -cp ",searchgui," eu.isas.searchgui.cmd.IdentificationParametersCLI -out ",i,".par -db   ",i,"_exp_fasta_for_searching_concatenated_target_decoy.fasta -frag_tol 0.05 -fixed_mods \"iTRAQ 8-plex of K,iTRAQ 8-plex of peptide N-term,Carbamidomethylation of C\" -variable_mods \"Acetylation of protein N-term,Deamidation of N,Oxidation of M\" -msgf_num_matches 1",sep=''))
    system(paste("java -cp ",searchgui," eu.isas.searchgui.cmd.SearchCLI -spectrum_files ",spectra_files," -id_params ",i,".par -output_folder ", output," -xtandem 1 -msgf 1 -tide 1  -output_default_name ",i,"_searchgui.out",sep=''))
    }

sgui_out1<-list.files(pattern="*zip")
sgui_out2<-list.files(pattern="*mgf$")
for (k in 1:length(sgui_out1)) {
    i<-sgui_out1[k]
    j<-sgui_out2[k] #check folder 
    system(paste("java -cp ",peptideshaker," eu.isas.peptideshaker.cmd.PeptideShakerCLI -experiment ",i," -sample ",i," -replicate 1 -identification_files ",output,"/",i," -spectrum_files ",spectra_files,"/",j," -out ",output,"/",i,".cpsx",sep=''))
    } #check input/output folder

pshaker_out<-list.files(pattern="*.cpsx$")
for(k in 1:length(pshaker_out)) {
    i=pshaker_out[k]
    system(paste("java -cp ",peptideshaker," eu.isas.peptideshaker.cmd.ReportCLI -in ",output,"/",i," -out_reports ",output," -reports 3,6,9",sep=''))
    }
