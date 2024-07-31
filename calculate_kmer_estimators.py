#!/usr/bin/env python

import argparse
import sys

from datetime import datetime
from pathlib import Path

from src.kmer import get_kmer_counts_dataframe
from src.dataframes import (merge_kmer_dataframes, calculate_kmer_count_diversity, 
                            calculate_kmer_count_specifity, calculate_sample_kmer_diversity,
                            calculate_sample_kmer_specifity,
                            rename_dataframe)


def parse_arguments():
    desc = "Create a table with "
    parser = argparse.ArgumentParser(description=desc)
    
    
    help_input = '''(Required) Directory with meryl counts.
                    Subolders have the suffix .count'''
    parser.add_argument("--input_dir", "-i", type=str,
                        help=help_input, required=True)
    
    help_hetkmers = "(optional) hetkmers_list"
    parser.add_argument("--hetkmers", "-k", type=str,
                        help=help_hetkmers, default="")
    
    help_output = "(Required) output dir"
    parser.add_argument("--output", "-o", type=str,
                        help=help_output, required=True)
    

    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


def get_arguments():
    parser = parse_arguments()
    inputs = [dir for dir in Path(parser.input_dir).glob("*.dump")]
    if parser.hetkmers:
        hetkmers_path = Path(parser.hetkmers)
    else:
        hetkmers_path = False
    return {"inputs": inputs,
            "output": Path(parser.output),
            "hetkmers": hetkmers_path}


def main():
    arguments = get_arguments()
    output_dir = arguments["output"]
    if not output_dir.exists():
        output_dir.mkdir(exist_ok=True, parents=True)
    if arguments["hetkmers"]:
        with open(arguments["hetkmers"]) as hetkmers_fhand:
            hetkmers = {kmers.split()[0]: kmers.rstrip().split()[1] for kmers in hetkmers_fhand}
    else:
        hetkmers = {}
    print("Kmer_counting_"+datetime.now().strftime("%d_%m_%Y-%H_%M_%S"))
    dataframes = [get_kmer_counts_dataframe(dir, hetkmers=hetkmers) for dir in arguments["inputs"]]
    print(dataframes)
    print("Merging_"+datetime.now().strftime("%d_%m_%Y-%H_%M_%S"))
    if len(dataframes) > 1:
        dataframe_by_kmer = merge_kmer_dataframes(dataframes)
    else:
        dataframe_by_kmer = dataframes[0]
    print(dataframe_by_kmer)
    print("Renaming_"+datetime.now().strftime("%d_%m_%Y-%H_%M_%S"))
    dataframe_by_kmer, index = rename_dataframe(dataframe_by_kmer)
    dataframe_by_sample = dataframe_by_kmer.T.iloc
    header =  dataframe_by_sample[0]
    dataframe_by_sample = dataframe_by_sample[1:]
    dataframe_by_sample.columns = header
    print("Diversity_sample_"+datetime.now().strftime("%d_%m_%Y-%H_%M_%S"))
    calculate_sample_kmer_diversity(dataframe_by_sample)
    calculate_sample_kmer_specifity(dataframe_by_sample)
    print("Diversity_kmer_"+datetime.now().strftime("%d_%m_%Y-%H_%M_%S"))
    calculate_kmer_count_diversity(dataframe_by_kmer)
    calculate_kmer_count_specifity(dataframe_by_kmer)
    dataframe_by_sample.to_csv(arguments["output"]/"estimators_by_sample.csv", sep="\t")
    dataframe_by_kmer.to_csv(arguments["output"]/"estimators_by_kmer.csv", sep="\t")
    with open(arguments["output"]/"kmer_index.tsv", "w") as index_fhand:
        for index_, kmer in index.items():
            index_fhand.write("{}\t{}\n".format(index_, kmer)) 
if __name__ == "__main__":
    main()