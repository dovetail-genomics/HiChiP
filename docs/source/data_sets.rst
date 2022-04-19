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

Data used for HiChIP Comparative Analysis (Mouse, mm10)
-------------------------------------------------------

.. _HCPD:

To get a list of all the files generated from the HiChIP Comparative Analysis tutorial, including the required reference genomes, you can use the command:

.. code-block:: console

   aws s3 ls s3://dovetail.pub/HiChIP/compare_samples/
 
Use wget to download any given file, replacing "s3://" with "https://s3.amazonaws.com/", followed by the remaining path to the file. For example:

.. code-block:: console

   wget https://s3.amazonaws.com/dovetail.pub/HiChIP/compare_samples/Reference_Genome/mm10.fa

+------------------+------------------------------------------------------------------------------------------------+
| Data Set         | Link                                                                                           |
+==================+================================================================================================+
| Fastqs           | - https://s3.amazonaws.com/dovetail.pub/HiChIP/compare_samples/fastq_inputs/sampleA_R1.fastq.gz|
| (Sample A)       | - https://s3.amazonaws.com/dovetail.pub/HiChIP/compare_samples/fastq_inputs/sampleA_R2.fastq.gz|
+------------------+------------------------------------------------------------------------------------------------+
| Fastqs           | - https://s3.amazonaws.com/dovetail.pub/HiChIP/compare_samples/fastq_inputs/sampleB_R1.fastq.gz|
| (Sample B)       | - https://s3.amazonaws.com/dovetail.pub/HiChIP/compare_samples/fastq_inputs/sampleB_R2.fastq.gz|
+------------------+------------------------------------------------------------------------------------------------+

Note: The full dataset, including input files and generated output is ~183Gb (roughly 5h with a network speed of 10Mb/s). 
