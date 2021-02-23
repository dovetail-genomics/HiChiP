#!/usr/bin/env python3

import argparse
import pysam
import numpy as np
import pandas as pd
from tabulate import tabulate

def get_read_count(bedfile):
    count = 0
    last_read = ''
    prev_id = ''
    reads = set()
    with open(bedfile,'r') as f:
        for line in f:
            attrs = line.split()
            read = attrs[3]
            reads.add(read)
    return len(reads)


def get_expected_observed(num_peaks, window_size, ref_length, reads_total, reads_observed):
    prob_read = num_peaks*window_size/ref_length
    expected_reads = prob_read*reads_total
    observed_expected_ratio = reads_observed/expected_reads
    return observed_expected_ratio


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b1',help="bedfile1") #500bp
    parser.add_argument('-b2',help="bedfile2") #1000bp
    parser.add_argument('-b3',help="bedfile3") #2000bp
    parser.add_argument('-peaks',help="input peaks")
    parser.add_argument('-bam',help="bamfile")
    args = parser.parse_args()


    in_500_peaks = get_read_count(args.b1)
    in_1000_peaks = get_read_count(args.b2)
    in_2000_peaks = get_read_count(args.b3)

    in_500_peaks_fmt = format(in_500_peaks,",d")
    in_1000_peaks_fmt = format(in_1000_peaks,",d")
    in_2000_peaks_fmt = format(in_2000_peaks,",d")

    bamfile = pysam.AlignmentFile(args.bam,'rb')

    paired_reads = 0


    bp_in_peaks = 0

    number_of_peaks = 0
    peak_size = []
    with open(args.peaks,'r') as f:
        for line in f:
            attrs = line.strip().split('\t')
            bp_in_peaks += int(attrs[2]) - int(attrs[1])
            peak_size.append(int(attrs[2]) - int(attrs[1]))
            number_of_peaks += 1

    ref_length = sum(bamfile.lengths)

    bp_outside_peaks = ref_length - bp_in_peaks

    total_no_reads = 0
    for r in bamfile.fetch(until_eof=True):
        total_no_reads += 1


    ratio_in_500_peaks = round(get_expected_observed(number_of_peaks,500, ref_length, total_no_reads, in_500_peaks), 2)
    ratio_in_1000_peaks = round(get_expected_observed(number_of_peaks,1000, ref_length, total_no_reads, in_1000_peaks),2)
    ratio_in_2000_peaks = round(get_expected_observed(number_of_peaks,2000, ref_length, total_no_reads, in_2000_peaks),2)


    in_500_peaks_p = round(in_500_peaks *100.0/total_no_reads,2)
    in_1000_peaks_p = round(in_1000_peaks *100.0/total_no_reads,2)
    in_2000_peaks_p = round(in_2000_peaks *100.0/total_no_reads,2)

    median_peak_size = format(int(np.median(peak_size)),",d")
    mean_peak_size = format(int(np.mean(peak_size)), ",d")
    number_of_peaks = format(number_of_peaks, ",d")

    table = []
    table.append(["Total ChIP peaks", number_of_peaks])
    table.append(["Mean ChIP peak size", f"{mean_peak_size} bp"])
    table.append(["Median ChIP peak size", f"{median_peak_size} bp"])
    table.append(["Total reads in 500 bp around center of peaks", f"{in_500_peaks_fmt}", f"{in_500_peaks_p}%"])
    table.append(["Total reads in 1000 bp around center of peaks", in_1000_peaks_fmt, f"{in_1000_peaks_p}%"])
    table.append(["Total reads in 2000 bp around summits", in_2000_peaks_fmt, f"{in_2000_peaks_p}%"])
    table.append(["Observed/Expected ratio for reads in 500 bp around center of peaks", ratio_in_500_peaks])
    table.append(["Observed/Expected ratio for reads in 1000 bp around center of peaks", ratio_in_1000_peaks])
    table.append(["Observed/Expected ratio for reads in 2000 bp around center of peaks", ratio_in_2000_peaks])
    print(tabulate(table,tablefmt="plain"))
