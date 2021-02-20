.. _1DPEAK:

Calling 1D peaks with MACS2 on HiChIP data
==========================================

Introduction
------------

Understanding where protein’s bind the DNA is a hallmark of ChIP-seq experiments. Typically, `MACS2 <https://github.com/macs3-project/MACS>`_  is used on ChIP-seq data to identify peak signal from the background noise and confirm where these binding sites are located. When it comes to HiChIP these binding sites (or anchors) are important to understand which molecule of the proximity-ligation step occurs at an anchor site or non-anchor site. This is information is used to QC the HiChIP library and is a requirement for identifying significant chromatin interactions. You may not have done any ChIP-seq work on a particular sample or maybe there is no publicly available data that reflects your specific sample type or experimental conditions. While it is most ideal to use ChIP-seq derived peak signals, it is possible to use the HiChIP data to call 1-dimensional peaks like you normally would in the ChIP-seq experiment. 

There are a few things to keep in mind when using HiChIP data to call 1-D peaks:
1.	You may be identifying secondary peaks along with the primary peaks (see figure below) and without a ChIP-seq dataset, it would be hard to discern one peak type from the other.
2.	Using ``.bam`` files that were processed and filtered through pairtools do not integrate nicely with MACS2. There is a simple solution for that which we will cover here.
3.	If you do call peaks with the HiChIP data, you should :ref:`run FitHiChIP <LPS>` on both peak-to-peak and peak-to-all settings.

.. image:: /images/1D.png


Input files
-----------

- :ref:`.bam <FINALBAM>` file generated at the :ref:`from fastq to final valid pairs bam file <FTB>` step.

.. admonition:: Testing!

   If you are looking for a dataset to practice this walkthrough, I reccomend the GM12878 CTCF (deep sequencing) from our publicaly available :ref:`datasets<DATASETS>`
   
Additional tools needed
-----------------------

- `MACS2 <https://github.com/macs3-project/MACS>`_

Workflow Overview
-----------------

1.	Select the primary alignment in the bam file and convert to bed format.
2.	Run MACS2.

Workflow
--------

1.	Select the primary alignment in the bam file and convert to bed format.

**Command:**

.. code-block:: console

   samtools –view –h –F 0x900 mapped.bam | bedtools bamtobed -i stdin > prefix.primary.aln.bed


Here we’re using samtools ``-view`` funtcion to retain the header (-h) and filter and keep (-F) the primary alignment (flag ID – 0X900) of the input bam file. Then the filtered alignments are being pipped into bedtools to convert the alignment (bam format) to bed format using the input flag for a UNIX piped input (stdin). Resulting in a final bed file. 


2.	Run MACS2.

**Command:**

.. code-block:: console
    
   Macs2 callpeak –t prefix.primary.aln.bed -n prefix.macs2 

Here we are using macs2 callpeak function the treatment file (-t) which is the primary alignment bed file, with a particular prefix assigned to the outputs (-n). 


