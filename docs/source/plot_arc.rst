.. _PARC:

Plotting HiChIP Data
====================

Introduction
------------

The purpose of this document is to provide a step-by-step walkthrough to plot significant interactions or “loops” generated through HiChIP data at regions of interests with minimal computational expertise, as seen in the figure below. This workflow assumes you have completed the previous steps :ref:`From fastq to final valid pairs bam file<FTB>`, :ref:`Library QC<LQ>` and :ref:`FitHiChIP Loop Calling<LPS>`. This guide will use the output bam file generated during the data processing and the merged interactions file from FitHiChIP walkthrough. We will be using the bioconductor package `Sushi in R <https://pubmed.ncbi.nlm.nih.gov/24903420/>`_ to plot both the coverage and contact arcs, as in the image below.

.. image:: /images/plot_intro_image.png

Inputs
------

- :ref:`Pairtools bam file<FINALBAM>`
- :ref:`FitHiChIP merged interactions output<FITOUT>` e.g. interactions_FitHiC_Q0.01_MergeNearContacts.bed

.. admonition:: Testing!

   If you are looking for a dataset to practice this walkthrough, I reccomend the GM12878 CTCF (deep sequencing) from our publicaly available :ref:`datasets<DATASETS>`


Tools and Data Used
-------------------

- `deepTools <https://deeptools.readthedocs.io/en/develop/content/installation.html>`_
- `R <https://www.r-project.org/>`_ with the following packages:

  - `Sushi <https://www.bioconductor.org/packages/release/bioc/html/Sushi.html>`_

Basic Workflow
--------------

The basic workflow is as follows:

1.	Converting the alignments to a contact matrix and a coverage bedgraph
2.	Open R and load libraries
3.	Import coverage bedgraph and merged contacts files into R and add a column for distance in merged contacts
4.	Set genomic regions 
5.	Plot and Print


Walkthrough
-----------

1.	Convert bam to bedgraph with deepTools
bamCoverage -b mapped.bam -of bedgraph -p 36 -o prefix.coverage.bedgraph

2.	Open R

**Command:**

.. code-block:: console

   R

3.	Load libraries

**Command:**

.. code-block:: r

   library("Sushi")


4.	Load data

**Command:**

.. code-block:: r

   cov <- read.table("prefix.coverage.bedgraph")
   arc <- read.table("prefix_ interactions_FitHiC_Q0.01_MergeNearContacts.bed", header=TRUE)

5.	Inspect arc file structure

**Command:**

.. code-block:: r

   head(arc)

.. image:: /images/plot_step5.png

Here we see that the structure of the significant interactions is structured like a bedpe file with position 1 as - chr1, start1, end1 and position 2 – chr2, start2, end2, make up the first six column entries. This is the key structure sushi needs to plot bedpe as “arcs“ or “loops”. 

The other key factor needed is the height of the arc that Sushi will plot. 
The rest of the columns point to stats regarding the interactions between position 1 and position 2 that could be used as a height scaler. A common way to plot HiChIP interactions that is visually pleasing is scale the height by the distance of the interaction, therefore we need to add a column of the distance between the start of position 1 and end of position 2

6. Add a column for distance in merged contacts file

**Command:**

.. code-block:: r

   arc$dist <- abs(arc$e2 - arc$s1)

7. Inspect arc file to see distance

**Command:**

.. code-block:: r

   head(arc)

.. image:: /images/plot_step7.png

8. Set region of interest for this example a 1.5 Mb region on chr8

**Command:**

.. code-block:: r

   chrom = "chr8"
   chromstart = 22500000
   chromend = 23200000

9.	Inspect coverage plot

**Command:**

.. code-block:: r

   plotBedgraph(cov,chrom,chromstart,chromend)
   labelgenome(chrom,chromstart,chromend,n=4,scale="Mb")
   mtext("Read Depth",side=2,line=1.75,cex=1,font=2)
   axis(side=2,las=2,tcl=.2)

.. image:: /images/plot_step9.png

10.	Plot arcs with arc heights based on distance

**Command:**

.. code-block:: r

   plotBedpe(arc,chrom,chromstart,chromend,heights = arc$dist,plottype="loops", flip=TRUE)
   labelgenome(chrom, chromstart,chromend,side=3, n=3,scale="Mb")
   axis(side=2,las=2,tcl=.2)
   mtext("distance",side=2,line=1.75,cex=.75,font=2)

.. image:: /images/plot_step10.png

While aesthetically pleasing, the arc file has much more informative information than the distance which is already captured on the x-axis. One could scale the height to the P or Q-values. Or could even add a color scale based on those statistical qualifiers (see the Sushi documentation for other variations on this). To demonstrate an additional layer of information in the arc plot, we can scale the arc height to the number of contacts interacting between position 1 and position 2. 

11.	Plot arcs with arc heights based on contact frequency

**Command:**

.. code-block:: r

   plotBedpe(arc,chrom,chromstart,chromend,heights = arc$sumCC,plottype="loops", flip=TRUE)
   labelgenome(chrom, chromstart,chromend,side=3, n=3,scale="Mb")
   axis(side=2,las=2,tcl=.2)
   mtext("contact freq",side=2,line=1.75,cex=.75,font=2)

.. image:: /images/plot_step11.png

Finally, we want to generate a PDF file for our records or to clean up in a PDF editor such as Adobe Illustrator. 

12.	Align and print both plots to a PDF file 

.. admonition:: Tip! 

   where "{}" I'd recommend pasting line-by-line rather than bulk copy and paste

**Command:**

.. code-block:: r

   pdfname <- "hichip.cov.arcs.pdf"
   makepdf = TRUE
   if(makepdf==TRUE) 
         {
         pdf(pdfname , height=10, width=12)
         }

   ##set layout
   layout(matrix(c(1, 
         2
         ), 2,1, byrow=TRUE)) 
   par(mgp=c(3,.3,0))

   ##plot coverage
   par(mar=c(3,4,2,2))
   plotBedgraph(cov,chrom,chromstart,chromend)
   labelgenome(chrom,chromstart,chromend,n=4,scale="Mb")
   mtext("Read Depth",side=2,line=1.75,cex=1,font=2)
   axis(side=2,las=2,tcl=.2)

   ##plot arcs with height based on contact frequency
   par(mar=c(3,4,2,2))
   plotBedpe(arc,chrom,chromstart,chromend,heights = arc$sumCC,plottype="loops", flip=TRUE)
   labelgenome(chrom, chromstart,chromend,side=3, n=3,scale="Mb")
   axis(side=2,las=2,tcl=.2)
   mtext("distance",side=2,line=1.75,cex=.75,font=2)

   if (makepdf==TRUE) 
   {
   dev.off() 
   }


The resulting figure should look like the one below:

.. image:: /images/plot_step12.png

**There’re figures, then there are Figures**
++++++++++++++++++++++++++++++++++++++++++++

The outlined workflow provides a rudimentary plot that illustrates the coverage and proximity-ligation links contained in HiChIP data. There is a lot more you can do to beautify the plots or to place the data in context of additional findings. In other words, there is more that should be done to generate a publishable figure. The Bioconductor package ‘Sushi’ has a plethora of ways to customize plots. Further documentation on this can be found `here <https://www.bioconductor.org/packages/release/bioc/vignettes/Sushi/inst/doc/Sushi.pdf>`_. Alternately the one could clean up the figure in a PDF editor, such as Adobe Illustrator. A few extra minutes in Illustrator provides the final figure below where contact arcs are plotted both by height in reference to the coverage (left) and by contact frequency (right):

.. image:: /images/plot_final.png


