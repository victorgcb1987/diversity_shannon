
## Requirements

**smudgeplot v0.2.5** : We recommend to use conda (`conda install smudgeplot==0.2.5`) to install this module.  

kmc https://github.com/refresh-bio/KMC. You will need to add kmc binaries to PATH variable for example using `export PATH=$PATH:kmc/install/bin/`

clone KATULU respository: `git clone https://github.com/victorgcb1987/KATULU.git`

## How to use 

### Omics diversity calculator
Omics diversity calculator is a pipeline that will calculate Shannon diversity index for files of your choice. These file can be fasta/fastq files or gene expression files like the ones provided by stringtie.

In order to runt this program you will need to prepare a file with table similar to this one:

| onegroup | R | transcriptome | 0 | 9999999999 | test1_r1.fastq.gz,test1_r2.fastq.gz |
|---|---|---|---|---|---|
| onegroup | R | transcriptome | 0 | 9999999999 | test2_r1.fastq.gz,test2_r2.fastq.gz |
| onegroup | G | genome | 0 | 9999999999 | test5.fasta.gz |
| othergroup | G | transcriptome | 0 | 999999999 | test4_r1.fastq.gz,test4_r2.fastq.gz |
| othergroup | E | expression | 0 | 000000000 | Petal.guided.abund.tsv |
| othergroup |E | expression | 0 | 000000000  |adult_vascular_leaf.guided.abund.tsv |
| anothergroup | G  |genome | 0 | 9999999999 | test5.fasta.gz |

The first and second columns are used to label group and subgroup respectively, for example to mark that one tissue in the first column and then a set of files of the same origin/class/etc. with the second column. 

The third column serves to label what kind of data is; you can put whaterver you like but if you use *** transcriptome *** hetkmers will be calculated and kmers and their values will be grouped using this. If you put *** expression ***, files will be treated as expression tables.

Fourth and fifth column are the minimun and the maximum values cutoff in order to consider a kmer or not in the analysis.

Sixth column is the filepaths column, you can separate different files with a comma.

This pipeline can be run with `omics_diversity_pipeline.py`and it accepts the following arguments:

  `--input_file INPUT_FILE, -i INPUT_FILE` (Required): the path to the table previously described
  
  `--output_dir OUTPUT_DIR, -o OUTPUT_DIR`(Required): the path were interemediate files and results will be stored. It will also check in this ouput for steps already done and will skip these steps.
  
  `--ram_usage RAM_USAGE, -r RAM_USAGE` (Optional, 1 by default): The max memory usage of kmc.
  
  `--num_threads NUM_THREADS, -t NUM_THREADS`(Optional 1 by default): Number of threads used by kmc.
  
  `--kmer_size KMER_SIZE, -k KMER_SIZE` (Optional, 21 by default): the kmer size used by kmc.
  
  `--merge_universe, -m` (Optional, False by default): This switchs whether if the kmer universe size should be calculated from all items from a group (True) or only for each sub group.
  
  `--presence, -p` (Optional, False by default) switchs change diversity calculation to presence/absence, counting all kmer count values to 1 if is present. For expression tables, a gene will throw a value of 1 if a gene has a TPM of 1 or more or 0 if its less than 1. 

