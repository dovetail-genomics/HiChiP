.. _DATASETS:

HiChIP Data Sets
================


To download one of the data sets, simply use the wget command:

.. code-block:: console

   wget https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/HiChiP_CTCF_2M_R1.fastq.gz
   wget https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/HiChiP_CTCF_2M_R2.fastq.gz
 
For testing purposes, we recommend using the 2M reads data sets, for any other purpose we recommend using the 800M reads data set.
 
Sequenced (human) libraries:
----------------------------

+------------------+---------------------------------------------------------------------------------+
| Library          | Link                                                                            |
+==================+=================================================================================+
| GM12878 CTCF 2M  | - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/HiChiP_CTCF_2M_R1.fastq.gz|
|                  | - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/HiChiP_CTCF_2M_R2.fastq.gz|
+------------------+---------------------------------------------------------------------------------+
| GM12878 CTCF     | - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/CTCF-DS_R1.fastq.gz       |
| (deep sequencing)| - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/CTCF-DS_R2.fastq.gz       |
+------------------+---------------------------------------------------------------------------------+
| GM12878 H3K27Ac  | - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/H3K27Ac_R1.fastq.gz       |
| (deep sequencing)| - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/H3K27Ac_R2.fastq.gz       |
+------------------+---------------------------------------------------------------------------------+
| GM12878 H3K4me3  | - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/H3K4me3_R1.fastq.gz       |
| (deep sequencing)| - https://s3.amazonaws.com/dovetail.pub/HiChIP/fastqs/H3K4me3_R2.fastq.gz       |
+------------------+---------------------------------------------------------------------------------+



Human, hg38, Peak files from ENCODE project
-------------------------------------------

.. csv-table::
   :file: tables/ENCODE_human.csv
   :header-rows: 1
   :widths: 12 12 12 40 24
   :class: tight-table
