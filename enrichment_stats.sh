#!/usr/bin/env bash
while getopts g:b:p:t:x: flag
do
        case "${flag}" in
                g) ref=${OPTARG};;
                b) bam=${OPTARG};;
                p) peaks=${OPTARG};;
                t) cores=${OPTARG};;
                x) prefix=${OPTARG};;
        esac
done
SRCDIR=`dirname $0`

OUTPUTFILE=${prefix}"_hichip_qc_metrics.txt"
TMPOUT=${prefix}"_hichip_qc_metrics.txt.tmp"


#compute how many reads intersect with peaks
awk '{$2=$2+$10-250;print}' ${peaks} | awk '{$3=$2+500;print}' | awk '{print $1"\t"$2"\t"$3}' > ${prefix}_tmp.bed
bedtools intersect -a ${bam} -b ${prefix}_tmp.bed -bed | sort -k4 > ${prefix}_peak_intersect_500.bed
awk '{$2=$2+$10-500;print}' ${peaks} | awk '{$3=$2+1000;print}' |  awk '{print $1"\t"$2"\t"$3}'> ${prefix}_tmp.bed
bedtools intersect -a ${bam} -b ${prefix}_tmp.bed -bed | sort -k4 | sort -k4 > ${prefix}_peaks_intersect_1000.bed
awk '{$2=$2+$10-1000;print}' ${peaks} | awk '{$3=$2+2000;print}' |  awk '{print $1"\t"$2"\t"$3}' > ${prefix}_tmp.bed
bedtools intersect -a ${bam} -b ${prefix}_tmp.bed -bed | sort -k4 > ${prefix}_peaks_intersect_2000.bed

wait


#print final stats
python ${SRCDIR}/count.py -b1 ${prefix}_peak_intersect_500.bed  -b2 ${prefix}_peaks_intersect_1000.bed \
        -b3  ${prefix}_peaks_intersect_2000.bed -bam ${bam} -peaks ${peaks} > ${TMPOUT}

cp ${TMPOUT} $OUTPUTFILE
rm ${TMPOUT}
rm ${prefix}_tmp.bed
