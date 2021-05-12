import os, sys, getopt, re, subprocess

# Ensure non-empty directory
def runTrinity(path):
    contents = os.listdir(path)
    r1_pattern = re.compile('(.*)_R1.fastq$') # search for fastq files ending in '_R1'
    for i in range(len(contents)):
        if r1_pattern.match(contents[i]):
            id = contents[i].split('_R1')
            if id[0]+'_R2.fastq' in contents: # ensures only paired reads
                print(id[0])
                file1 = path + "/" + id[0] + "_R1.fastq"
                print(file1)
                file2 = path + "/" + id[0] + "_R2.fastq"
                print(file2)
                os.system(f"Trinity --seqType fq --normalize_by_read_set --left {file1} --right {file2} --trimmomatic --full_cleanup --CPU 30 --max_memory 50G --bflyCPU 10 --bflyHeapSpaceMax 4G --output {path}/Trinity.{id[0]} --monitoring --verbose")

def nonEmpty(path):
    if not os.listdir(path):
        sys.exit("Directory %s is empty." %path)
    else:
        runTrinity(path)            

    