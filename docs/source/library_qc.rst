.. _LQ:

Library QC
==========

Proximity-ligation assessment
-----------------------------

At step :ref:`Removing PCR duplicates<DUPs>` you used the flag `--output-stats`, generating a stats file in addition to the pairsam output (e.g. --output-stats stats.txt). The stats file is an extensive output of pairs statistics as calculated by pairtools, including total reads, total mapped, total dups, total pairs for each pair of chromosomes etc'. Although you can use directly the pairtools stats file as is to get informed on the quality of the HiChiP library, we find it easier to focus on a few key metrics. We include in this repository the script `get_qc.py` that summarize the paired-tools stats file and present them in percentage values in addition to absolute values.

The images below explains how the values on the QC report are calculated:

.. image:: /images/QC_align.png

.. image:: /images/QC_cis_trans_valids.png

**Command:**

.. code-block:: console

   python3 ./HiChiP/get_qc.py -p <stats.txt>


**Example:**

.. code-block:: console

   python3 ./HiChiP/get_qc.py -p stats.txt 


After the script completes, it will print:

.. code-block:: console

   Total Read Pairs                              2,000,000  100%
   Unmapped Read Pairs                           92,059     4.6%
   Mapped Read Pairs                             1,637,655  81.88%
   PCR Dup Read Pairs                            5,426      0.27%
   No-Dup Read Pairs                             1,632,229  81.61%
   No-Dup Cis Read Pairs                         1,288,943  78.97%
   No-Dup Trans Read Pairs                       343,286    21.03%
   No-Dup Valid Read Pairs (cis >= 1kb + trans)  1,482,597  90.83%
   No-Dup Cis Read Pairs < 1kb                   149,632    9.17%
   No-Dup Cis Read Pairs >= 1kb                  1,139,311  69.8%
   No-Dup Cis Read Pairs >= 10kb                 870,490    53.33%



We consider a library prepared from a **mammalian** sample to be acceptable if:
- Mapped nondupe pairs cis > 1,000 bp is greater than 20% of the total mapped nondupe pairs.


ChiP enrichment
---------------

Another key step in evaluating the quality of the HiChiP library is assesing the enrichment of HiChiP reads at protein binding sites, when protein binding sites correspond to a list of Chip-seq peaks. You can obtain gold-standards Chip-Seq peaks from databases, such as ENCODE, or generate your own list of peaks based on ChiP-Seq experiments, e.g. using :ref: `MACS2 <https://hbctraining.github.io/Intro-to-ChIPseq/lessons/05_peak_calling_macs.html>`. 


To calculate stats of read enrichment around ChIP peak, we provide the enrichment_stats.sh which takes as an input the genome file, final bam file and peak file and output the read enrichment around ChIP-seq peaks

**Command:**

.. code-block:: console

   ./HiChiP/enrichment_stats.sh -g <ref.genome> -b <mapped.PT.bam> -p <peaks.bed> -t <cores> -x <prefix>


**Example:**

.. code-block:: console

   ./HiChiP/enrichment_stats.sh -g hg38.genome -b mapped.PT.bam -p ENCFF017XLW.bed -t 16 -x CTCF


In this example an output file `CTCF_hichip_qc_metrics.txt` will be created  with the below information:


.. code-block:: console

   Total ChIP peaks                                                     41,017
   Mean ChIP peak size                                                  309 bp
   Median ChIP peak size                                                356 bp
   Total reads in 500 bp around center of peaks                         393,163  9.46%
   Total reads in 1000 bp around center of peaks                        519,272  12.49%
   Total reads in 2000 bp around summits                                692,305  16.66%
   Observed/Expected ratio for reads in 500 bp around center of peaks   14.25
   Observed/Expected ratio for reads in 1000 bp around center of peaks  9.41
   Observed/Expected ratio for reads in 2000 bp around center of peaks  6.27

