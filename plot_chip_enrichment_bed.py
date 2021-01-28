#!/usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import subprocess

'''
chr1    826678  826954  
chr1    958283  959249 
chr1    1115852 1116138
chr1    1157596 1158571
chr1    1230531 1231969
chr1    1324817 1326133
'''

parser = argparse.ArgumentParser()
parser.add_argument("-bam", help="Input BAM file")
parser.add_argument("-peaks", help="ChiSeq peaks 3 columns bed format")
parser.add_argument("-output", help="Output file")

args = parser.parse_args()

peak_data = pd.read_csv(args.peaks, sep="\t", header=None, keep_default_na=False)
peak_data.columns = ["chromosome", "start", "end"]

count = 0

coverage = dict()

for i in range(-1000, 1001):
    coverage[i] = 0

count = 0
for num, row in peak_data.iterrows():
    chrom = row["chromosome"]
    center = round((row["start"] + row["end"]) / 2)
    start  = center - 1000
    end = center + 1000
    x = []
    y = []
    count += 1
    proc = subprocess.Popen(['samtools','mpileup', '-A', args.bam, '-r', f"{chrom}:{start}-{end}"],stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode('ascii')
        if not line: 
            break
        attrs = line.split('\t')
        pos = int(attrs[1])
        coverage[pos - center] += int(attrs[3])

x = list(coverage.keys())
y = list(coverage.values())
x_ticks = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000] 
x_labels = ["-1000 bp", "-750 bp", "-500 bp", "-250 bp", "0 bp", "+250 bp", "+500 bp", "+750 bp", "+1000 bp"]

y = [float(i)/np.mean(y) for i in y]
plt.xticks(ticks=x_ticks, labels=x_labels, fontsize=7)
plt.grid()
plt.plot(y)
plt.title("Coverage around ChIP peaks")
plt.xlabel("Distance from the peak center")
plt.ylabel("Fold coverage change  based on average coverage")
plt.savefig(args.output, dpi=300)
