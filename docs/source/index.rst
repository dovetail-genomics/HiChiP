.. HiChIP documentation master file, created by
   sphinx-quickstart on Sun Jan 24 01:50:52 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. image:: /images/DOV_FINAL_LOGO_2017_RGB.svg
   :width: 100pt


Welcome to HiChIP documentation
================================


.. image:: /images/hichip-kit_gw.png
  

Overview
========
- The Dovetail™ HiChIP MNase Kit combines the benefits of ChIP-seq with Hi-C, a proximity ligation method that captures long-range interactions using standard Illumina paired-end sequencing, enabling researchers to query protein-directed chromatin conformation mediated by specific proteins of interest.

- Key benefits of HiChIP:

  - Capture ChIP-seq and Hi-C data together in a single library
  - Map chromatin interactions at nucleosome level resolution
  
- The unique combination of the Dovetail™ Micro-C Proximity Ligation Assay with the Dovetail HiChIP approach enables the use of micrococcal nuclease (MNase) to fragment chromatin uniformly and without sequence bias prior to proximity ligation, eliminating the need for finicky sonication procedures and offering the maximal resolution (down to mono-nucleosome size) of chromatin interactions.

- Enrichment of protein-directed chromatin features enables high-resolution contact map generation with less read depth. Compared to a high resolution restriction enzyme-based Hi-C, Dovetail HiChIP data enables visualization of higher-order chromatin features, such as loops and chromatin interactions, at a fraction of the read depth leading to significant sequencing costs savings.

- This guide will take you step by step on how to QC your HiChIP library, how to interparate the QC results and how to call and plot significant interactions. If you don't yet have a sequenced HiChIP library and you want to get familiar with the data, you can download HiChIP sequences libraries from our publicaly available :ref:`data sets<DATASETS>`.

- The QC process starts with aligning the reads to a reference genome then retaining high quality mapped reads. From there the mapped data will be used to generating a pairs file with pairtools, which categorizes pairs by read type and insert distance, this step both flags and removes PCR duplicates. Once pairs are categorized, counts of each class are summed and reported.

- If this is your first time following this tutorial, please check the :ref:`Before you begin page <BYB>` first.

.. raw:: html

   <iframe src="https://player.vimeo.com/video/453644547" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>

.. raw:: html

   <iframe src="https://player.vimeo.com/video/478256620" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
   
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   before_you_begin
   
   pre_alignment
   
   fastq_to_bam
   
   library_qc
   
   contact_map

   loops

   hichip_compare

   plot_arc

   1D_peak
   
   data_sets

   support
.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
