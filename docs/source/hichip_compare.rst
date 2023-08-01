.. _HCOMP:

HiChIP Comparative Analyses
===========================

Introduction
------------

Biological questions are seldom answered by analysing single samples in isolation. It is often the case that an experiment aims to make comparisons between two (or more) biological conditions,
such as:

1)	Untreated wild type vs treatment
2)  Wild type vs knockout
3)  Normal sample vs tumor

In all cases the goal is to produce a list of differentially interacting regions in one condition relative to the other. The main output for comparitive analses is analogous to what is expeected for differential gene expression,
where the primary result is a table of regions, the fold change between conditions, and a statistical measure of signficance. For HiCHiP, the unit for comparison are the loop calls identified using the FitHiChIP software as described
in :ref:`previous steps <LPS>`. 

Figure 1:

.. image:: /images/CA_fig1.png


Differential Analysis
---------------------

**Question:** How do I perform differential analyses for HiChIP?

**Process:** Results files from FitHiChIP are used to construct a differential design, and comparison is performed using the scripts bundled with fithichip software.

**Results:** Final results consist of a table of differentially interacting regions, fold change, and measure of statistical signficance.

**Files and tools needed:**
  - FitHiChIP loop calls for each condition: *PREFIX*.interactions_FitHiC.bed
  - `FitHiChIP <https://github.com/ay-lab/FitHiChIP>`_ differential analysis software and scripts
  - Associated ChIP-seq peak files [optional]

As the design of differential analysis experiments are unique to each biological question, there are multiple possibilites for how the analysis can be set up. A common scenario is to compare two conditions
where each condition has two replicates, and is described in the `FitHiChIP documentation pages`.

**Interpreting results:**

FitHiChIP differential analysis produces a number of intermediate in addition to the final results table. The most important is the list of significant loops and is named "Loops_EdgeR_Default_SIG.bed".
In general, the interpretation of differential loop analysis is the same as what is familiar for gene expression analysis, where intereactions can be prioritized based on the fold change and statistical significance.
An example output file is given below.

.. csv-table::
   :file: tables/CA_results.csv
   :header-rows: 1
   :widths: 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12
   :class: tight-table

The most relevant fields from the output will be:
  - logFC -- the log fold change in coverage between the two conditions
  - FDR -- a p-value, after correction for multiple hypothesis testing, on the statistical signficance of the observed fold change

**Considerations:**

   - Replication – It is generally advisable to have technical replicates for differential analyses, as this will produce more statistically robust results. FitHiChIP is still able to perform differential analysis with single-replicate samples, and in this case reverts to the square-root-dispersion method used by EdgeR.
   - Paired ChIP-seq experiments – As mentioned above, it is best practices to have paired ChIP-seq experiments. If that is not do-able, FitHiChIP is bundled with a script that can call peaks de novo from the HiChIP data directly.
