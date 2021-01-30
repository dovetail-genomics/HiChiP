.. _LQ:

Library QC
==========

Proximity-ligation assessment
-----------------------------

At step :ref:`Removing PCR duplicates<DUPs>` you used the flag `--output-stats`, generating a stats file in addition to the pairsam output (e.g. --output-stats stats.txt). The stats file is an extensive output of pairs statistics as calculated by pairtools, including total reads, total mapped, total dups, total pairs for each pair of chromosomes etc'. Although you can use directly the pairtools stats file as is to get informed on the quality of the HiChiP library, we find it easier to focus on a few key metrics. We include in this repository the script ``get_qc.py`` that summarize the paired-tools stats file and present them in percentage values in addition to absolute values.

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
   Unmapped Read Pairs                           75,832     3.79%
   Mapped Read Pairs                             1,722,285  86.11%
   PCR Dup Read Pairs                            4,507      0.23%
   No-Dup Read Pairs                             1,717,778  85.89%
   No-Dup Cis Read Pairs                         1,385,238  80.64%
   No-Dup Trans Read Pairs                       332,540    19.36%
   No-Dup Valid Read Pairs (cis >= 1kb + trans)  875,804    50.98%
   No-Dup Cis Read Pairs < 1kb                   841,974    49.02%
   No-Dup Cis Read Pairs >= 1kb                  543,264    31.63%
   No-Dup Cis Read Pairs >= 10kb                 193,061    11.24%


We consider a library prepared from a **mammalian** sample to be acceptable if:
- Mapped nondupe pairs cis > 1,000 bp is greater than 20% of the total mapped No-Dup pairs.

.. _CENRICH:

ChiP enrichment
---------------

Calculating enrichment stats
++++++++++++++++++++++++++++

Another key step in evaluating the quality of the HiChiP library is assessing the enrichment of HiChiP reads at protein binding sites, when protein binding sites correspond to a list of ChiP-Seq peaks. 

Our QC pipeline supports as an input both peaks in a simple ``bed`` file format (containing three columns: chr, star, end) or `ENCODE narrow peak format <https://genome.ucsc.edu/FAQ/FAQformat.html#format12>`_. For your convenience we include here :ref:`links<DATASETS>` to some key examples of peak files from ENCODE ChiP-Seq experiments. All are of proteins for which Dovetail™ HiChIP MNase Kit has `validated antibodies <https://dovetailgenomics.com/hichip-validated-antibodies/>`_.

You can obtain gold-standards Chip-Seq peaks from databases, such as ENCODE, or generate your own list of peaks based on ChiP-Seq experiments, e.g. using `MACS2 <https://hbctraining.github.io/Intro-to-ChIPseq/lessons/05_peak_calling_macs.html>`_. 

To calculate stats of reads enrichment around ChIP peaks, we provide the ``enrichment_stats.sh`` script:

.. admonition:: Reminder!

   Did you remember to make the ``enrichment_stats.sh`` script executable?

   If not, run the following command:

   .. code-block:: console

     chmod +x ./HiChiP/enrichment_stats.sh

   If you already ran this command, no need to run it again the execution permission is saved



+---------+----------------------------------------------------------------------------------------+
|Parameter|Function                                                                                |
+=========+========================================================================================+
|-g       |Input :ref:`genome file<GENOME>`                                                        |
+---------+----------------------------------------------------------------------------------------+
|-b       |Input :ref:`final bam file<FINALBAM>`                                                   |
+---------+----------------------------------------------------------------------------------------+
|-p       |Input (either in asimple bed format or narrow peak format)                              |
+---------+----------------------------------------------------------------------------------------+
|-t       |no. of threads                                                                          |
+---------+----------------------------------------------------------------------------------------+
|-x       |Prefix for output file, enrichment stats will be saved to <prefix>_hichip_qc_metrics.txt|
+---------+----------------------------------------------------------------------------------------+


**Command:**

.. code-block:: console

   ./HiChiP/enrichment_stats.sh -g <ref.genome> -b <mapped.PT.bam> -p <peaks.bed> -t <cores> -x <prefix>


**Example:**

.. code-block:: console

   ./HiChiP/enrichment_stats.sh -g hg38.genome -b mapped.PT.bam -p ENCFF017XLW.bed -t 16 -x CTCF

.. admonition:: Tip!

   If your peak file is zipped make sure to unzip it before running the ``enrichment_stats.sh`` script, e.g.:

   .. code-block:: console

      gunzip peak.bed.gz

In this example an output file `CTCF_hichip_qc_metrics.txt` will be created  with the below information:


.. code-block:: console

   Total ChIP peaks                                                     41,017
   Mean ChIP peak size                                                  309 bp
   Median ChIP peak size                                                356 bp
   Total reads in 500 bp around center of peaks                         321,368  7.91%
   Total reads in 1000 bp around center of peaks                        458,843  11.3%
   Total reads in 2000 bp around summits                                673,628  16.59%
   Observed/Expected ratio for reads in 500 bp around center of peaks   11.92
   Observed/Expected ratio for reads in 1000 bp around center of peaks  8.51
   Observed/Expected ratio for reads in 2000 bp around center of peaks  6.25

The following image illustrates how enrichment around ChiP-Seq peaks is calculated:

.. image:: /images/Step1.png
   :width: 500pt

.. image:: /images/Step2a.png
   :width: 500pt

.. image:: /images/Step2bc.png
   :width: 500pt

Plotting global enrichment around ChiP peaks
++++++++++++++++++++++++++++++++++++++++++++

The ``plot_chip_enrichment.py`` and ``plot_chip_enrichment_bed.py`` scripts provide global evaluation of enrichment around known ChiP peaks. The script identifies the regions of ChiP peaks, sets a window of 1kb upstream and downstream of the peak's center, and based on the :ref:`bam file<FINALBAM>` of the valid pairs, calculates the aggregated read coverage within this window and plots the global fold coverage change based on the observed coverage divided by the mean coverage, as :ref:`illustrated<CHIPIMAGE>`. 

``plot_chip_enrichment.py`` is intendent to be used when a ``narrowPeak`` file is available and ``plot_chip_enrichment_bed.py`` accept a simple ``bed`` file with peaks intervals as an input. Other than that, the two scripts accept the same parameters:

+---------+----------------------------------------------------------------------------------------+
|Parameter|Function                                                                                |
+=========+========================================================================================+
|-bam     |Input :ref:`final bam file<FINALBAM>`                                                   |
+---------+----------------------------------------------------------------------------------------+
|-peaks   |Input peaks in ``narrowPeak`` format (``plot_chip_enrichment.py``) or                   |
|         |in simple chr,start,end ``bed`` format (plot_chip_enrichment_bed.py)                    |
+---------+----------------------------------------------------------------------------------------+
|-output  |ouptput file name to save the enrichment plot .png image                                |
+---------+----------------------------------------------------------------------------------------+

**Command:**

.. code-block:: console

   python3 plot_chip_enrichment.py -bam <mapped.PT.bam> -peaks <peaks.bed> -output <enrichment.png>

or 

.. code-block:: console

   python3 plot_chip_enrichment_bed.py -bam <mapped.PT.bam> -peaks <peaks.bed> -output <enrichment.png>


**Example:**

.. code-block:: console

   python3 ./HiChiP/plot_chip_enrichment.py -bam mapped.PT.bam -peaks ENCFF017XLW.bed -output enrichment.png

or 

..code-block:: console

  python3 ./HiChiP/plot_chip_enrichment_bed.py -bam mapped.PT.bam -peaks peaks.bed -output enrichment.png


Output plot:

.. image:: /images/enrichment_narrow.png

.. admonition:: Important!

   - ``plot_chip_enrichment.py`` will accept only ``narrowPeak`` format which has to include 10 columns, with the following specifications:
     - chromosome, start, end, in the three first columns 
     - Peak Signal value at column #7
     - Peak offset value at column #10 (when offset is the distance between the start position and the center of the peaks)

   - If your peak file does not follow the above structure you can modify it into a simple bed file by extracting only the three first columns into a new file that can be used with the plot_chip_enrichment_bed.py script. 

   - ``plot_chip_enrichment_bed.py`` will accept only bed files with 3 columns. If your bed file includes more than three columns, extract the three first columns into a new file

   - Example, how to extract only the first three columns:

     .. code-block:: console

        cut -f1,2,3 input.bed > output.bed

There are two minor differences between the two scripts: 

- ``plot_chip_enrichment.py`` calculates the center of the peak according to ``start + offset`` 
  ``plot_chip_enrichment_bed.py`` chooses the center of the peak as the middle point between ``start`` and ``end``. 
  Both will calculate the aggregated enrichment -1kb and +1kb of the center of the peak (no matter the legnth of the peak)

- All intervals in the bed files are used for the meta-analysis when ``plot_chip_enrichment_bed.py`` is used
  ``narrowPeak`` format includes information on peak signal, this information is used to filter out peaks with extreme values (either very low or very high signals) prior to meta-analysis
 
.. _CHIPIMAGE:

.. image:: /images/Step3.png
   :width: 500pt
