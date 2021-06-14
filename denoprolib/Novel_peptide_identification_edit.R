#!/usr/bin/Rscript
args <- commandArgs(TRUE)

library(plyr)
library(dplyr)
library(tidyr)
library(data.table)
library(XML)

output_dir = args[1]
actg_dir = args[2]
mapping_method = args[3]
proteindb = args[4]
ser_file = args[5]
ref_genome = args[6]

setwd(output_dir)

peptide_report<-list.files(pattern="*Peptide_Report.txt",recursive=TRUE)
psm_report<-list.files(pattern="*PSM_Report.txt",recursive=TRUE)

for (k in 1:length(peptide_report)){
	r1<-read.delim(peptide_report[k])
	print(peptide_report[k])
	r2<-subset(r1, !grepl("^NP_", r1$Protein.s.))
	r3<-r2[!duplicated(r2$Sequence),]
	r3<-subset(r3,Validation=="Confident")
	r4<-read.delim(psm_report[k])
	print(psm_report[k])

	m<-merge(r4,r3,by="Sequence")
	m1<-m[,c("Sequence","Protein.s..x","Modified.Sequence.x","Variable.Modifications.x","Fixed.Modifications.x","Spectrum.Title","Confidence.....x","Validation.x")]
	m2<-subset(m1,Validation.x=="Confident")
	
    list <- strsplit(as.character(peptide_report[k]), split="/")
	df <- ldply(list)
	write.csv(m2,file=paste("Novel_Confident_Peptides_PSMs",df$V1,'csv',sep='.'))
	}

conf_peptide_psm<-list.files(pattern="^Novel_Confident_Peptides_PSMs",recursive=TRUE)

for (k in 1:length(conf_peptide_psm)) {
	r1<-read.csv(conf_peptide_psm[k])
	print(conf_peptide_psm[k])
	r2<-r1[!duplicated(r1$Sequence),]
	list <- strsplit(as.character(conf_peptide_psm[k]), split="/")
	df1 <- ldply(list)
	r3<-r2$Sequence
	r3<-as.data.frame(r3)
	write.table(r3,row.names=F,col.names = F,quote=FALSE,file=paste("novel_peptides_for_ACTG",df1$V1,'txt',sep='.'))
	}

peptide_for_actg<-list.files(pattern="^novel_peptides_for_ACTG",recursive=TRUE)

# Edit and prepare ACTG's mapping_params.xml
data <- xmlParse(actg_dir,"/mapping_params.xml")

invisible(replaceNodes(data[["//Environment/MappingMethod/text()"]], newXMLTextNode(mapping_method)))
invisible(replaceNodes(data[["//Environment/Output/text()"]], newXMLTextNode(output_dir)))
invisible(replaceNodes(data[["//ProteinDB/Input/text()"]], newXMLTextNode(proteindb)))
invisible(replaceNodes(data[["//VariantSpliceGraph/Input[@type='graphFile']/text()"]], newXMLTextNode(ser_file)))
invisible(replaceNodes(data[["//SixFrameTranslation/Input/text()"]], newXMLTextNode(ref_genome)))


for (k in 1:length(peptide_for_actg)) {
#	data <- xmlParse(actg_dir,"/mapping_params.xml")
	invisible(replaceNodes(data[["//Input/text()"]], newXMLTextNode(peptide_for_actg[k])))
	list <- strsplit(as.character(peptide_for_actg[k]), split="/")
	df1 <- ldply(list)
	saveXML(data,file=paste(df1$V1,'xml',sep='.'))
	}


xml_out<-list.files(pattern="*txt.xml",recursive=TRUE)
for (k in 1:length(xml_out)) {
	i<-xml_out[k]
	print(i)
	cmd<-paste("java -Xmx8G -Xss2m -jar ",actg_dir,"/ACTG_mapping.jar ",i)
	system(cmd)
	}

flat_out<-list.files(pattern="*.flat$",recursive=TRUE)
gff_out<-list.files(pattern="*.gff$",recursive=TRUE)
for (k in 1:length(flat_out)) {
	r1<-read.delim(flat_out[k])
	print(flat_out[k])
	single<-names(which(table(r1$Peptide)==1))
	r2<-r1[r1$Peptide %in% single,]
	write.csv(r2,file=paste(flat_out[k],'csv',sep='.'))
	r3<-read.delim(gff_out[k],header=F)
	list <- strsplit(as.character(r3$V9), split="=")
	df <- ldply(list)
	library(plyr)
	df <- ldply(list)
	r3$GFFID<-df$V2
	r5<-merge(r2,r3,by="GFFID")
	write.csv(r5,paste(flat_out[k],"ACTG_peptides_gff_combined",'csv',sep='.'))
	}

nov_conf_pep_psm<-list.files(pattern="^Novel_Confident_Peptides_PSMs(.*)txt.csv$",recursive=TRUE)
actg_pep_gff<-list.files(pattern="*ACTG_peptides_gff_combined.csv",recursive=TRUE)
for(k in 1:length(nov_conf_pep_psm)) {
	r1<-read.csv(nov_conf_pep_psm[k])
	r2<-read.csv(paste(actg_pep_gff[k],sep=''))
	colnames(r2)[which(names(r2) == "Peptide")] <- "Sequence"
	m<-merge(r2,r1,by="Sequence")
	write.csv(m,paste(nov_conf_pep_psm[k],"combined_ACTG_peptides_PSMs",'csv',sep='.'))
	}

system(find . -name "*.combined_ACTG_peptides_PSMs.csv" -exec cat {} \;> ALL_NOVEL_PEPTIDES_ATCG.csv)

r1<-read.csv("ALL_NOVEL_PEPTIDES_ATCG.csv")
r2<-r1[!duplicated(r1$Spectrum.Title),]
r3<-count(r2,'Sequence')
m<-merge(r3,r1,by="Sequence")
r4<-r2[!duplicated(r2$Sequence),]
r5<-count(r4,'GeneID')
m1<-merge(m,r5,by="GeneID")
write.csv(m1,"GENE_PEPTIDE_FILE_NUMBER_OF_PSMs_PEPTIDE_All.csv")
