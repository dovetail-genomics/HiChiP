.. _HCOMP:

HiChIP Comparative Analyses
===========================

.. raw:: html
  
  <video width="720" height="480" controls>
   <source src="https://s3.amazonaws.com/dovetail.pub/HiChIP/compare_samples/HiChIP_Compare_RTD_workshop.mov">
  </video> 


Introduction
------------

Answering biological questions with proximity-ligation data might seem challenging at first glance. However, once the data are converted into simplified tables, very standard data analysis theory can be applied in basic computing language. This document aims to provide an example and clearly outline the steps used to compare HiChIP data sets from different experimental conditions. Here we use open-source proximity-ligation tools combined with standard analytical approaches in the statistical package R to identify differential interactions between a wildtype (Sample A) and treated sample (Sample B). This will be achieved by asking a series of basic question of the data, providing the code the address that question, then summarizing the results. We will be following the workflow as outlined in Figure 1 and asking the following questions:

1)	How to I process the data?
2)	Do the data look good?
3)	Can differential HiChIP interactions be detected?
4)	Do the contact matrices support the loop analysis?
5)	What functions are enriched in those differential loops?
6)	Which genes within those functions should highlighted?
7)	How does looping at both conditions behave at those genes?

It should be noted that apart from the QC steps, these tools are open-sourced and not owned or managed by Dovetail Genomics. As such any errors or trouble shooting that should be required for the installation or execution of any of these tools should be through the github pages of those tools, not by Dovetail Genomics. 

The main goal of this tutorial is to get you comfortable with the data structure and format, and to teach you how to ask questions of chromatin interaction data. This is an example of how one could go from fastq to learning what functions and genes are specifically associated with looping across at wildtype-treatment experimental design. Ideally once you have completed this workflow you should be able to ask your own question of loop data!

Figure 1:

.. image:: /images/Fig1_Overview.png

Data Access
-----------

For access to all input files, including sample A and B fastqs, reference genomes, and example output used in this tutorial, please see the :ref:`datasets section <HCPD>`.

Experimental Design
-------------------

Cultured mouse cells were subjected to an experimental condition. Ten million wildtype cells (sample A) and treated cells (sample B) where grown, isolated, and flash frozen. The cells were divided into two - 5 million technical replicates and Dovetail genomics MNase-HiChIP was performed against H3K27ac antibody resulting in four libraries (two per condition). Libraries were sequenced to ~100 million total read pairs (2x150bp) and the resulting fastqs were merged prior to data processing with the cat command in linux.

1. Data Processing
------------------
**Question:** How do I process these data?

**Process:** Merged fastqs were aligned with bwa mem -5SP and deduplicated and converted into both alignment files (.bam) and pairs coordinate files (.pairs) following the best practices (https://hichip.readthedocs.io/en/latest/fastq_to_bam.html). Valid pairs were converted into contact matrices (.cool) with cooler cload pairix function. Finally, to prepare for subsequent analyses, coverage bedgraph files were generated from the bam file using deepTools bamCoverage, normalized to RPKM. Since these HiChIP experiments do not have the recommended paired ChIP-seq experiments, the primary alignment was isolated and converted into bed format, then peaks are called with macs2. Computational Steps for this section are outlined in steps 1.1 – 1.6. This step can take about 12-24 hours of compute hours.

**Results:** Through the data processing we know have alignments, pair files, contact matrices, alignment files, and narrowPeak files that required for downstream analyses. This workflow generated all the file types denoted by grey boxes in Figure 1. We have also generated 1D peak files as denoted in the purple box in Figure 1. 

**Tools needed:**
  - bwa
  - pairtools
  - samtools
  - deepTools
  - pairix
  - cooler
  - bedtools
  - macs2

**Commands:**

- 1.1 Align, parse pairs to get bam and pairs file

.. code-block:: console

  bwa mem -5SP -T0 -t32 mm10.fa sampleA_R1.fastq.gz sampleA_R2.fastq.gz | pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 32 --nproc-out 32 chroms-path mm10.genome | pairtools sort --tmpdir=temp/ --nproc 32|pairtools dedup --nproc-in 32 --nproc-out 32 --mark-dups --output-stats  sampleA.txt|pairtools split --nproc-in 32 --nproc-out 32 --output-pairs  sampleA.pairs.gz --output-sam -|samtools view -bS -@32 | samtools sort -@32 -o  sampleA.bam;samtools index sampleA.bam
  bwa mem -5SP -T0 -t32 mm10.fa sampleB_R1.fastq.gz sampleB_R2.fastq.gz | pairtools parse --min-mapq 40 --walks-policy 5unique --max-inter-align-gap 30 --nproc-in 32 --nproc-out 32 chroms-path mm10.genome | pairtools sort --tmpdir=temp/ --nproc 32|pairtools dedup --nproc-in 32 --nproc-out 32 --mark-dups --output-stats  sampleB.txt|pairtools split --nproc-in 32 --nproc-out 32 --output-pairs  sampleB.pairs.gz --output-sam -|samtools view -bS -@32 | samtools sort -@32 -o  sampleB.bam;samtools index sampleB.bam

- 1.2 Make bedgraphs from bam files

.. code-block:: console

  bamCoverage --normalizeUsing RPKM -of bedgraph --ignoreDuplicates -bs 50 -p 16 -b sampleA.bam -o sampleA.RPKM.bedgraph
  bamCoverage --normalizeUsing RPKM -of bedgraph --ignoreDuplicates -bs 50 -p 16 -b sampleB.bam -o sampleB.RPKM.bedgraph

- 1.3 Convert to hicpro format, by re-ordering the columns, for FitHiChIP loop calling

.. code-block:: console

  zcat sampleA.pairs.gz | grep -v '#' | awk -F"\t" '{print $1"\t"$2"\t"$3"\t"$6"\t"$4"\t"$5"\t"$7}' | gzip -c >sampleA.hicpro.pairs.gz
  zcat sampleA.pairs.gz | grep -v '#' | awk -F"\t" '{print $1"\t"$2"\t"$3"\t"$6"\t"$4"\t"$5"\t"$7}' | gzip -c >sampleA.hicpro.pairs.gz

- 1.4.1 index pairs

.. code-block:: console

  pairix sampleA.pairs.gz
  pairix sampleB.pairs.gz

- 1.4.2 make 5kb matrices

.. code-block:: console

  cooler cload pairix -p 24 mm10.geome:5000 sampleA.pairs.gz sampleA.5kb.cool
  cooler cload pairix -p 24 mm10.geome:5000 sampleB.pairs.gz  sampleB.5kb.cool


- 1.5 Get primary alignment from the bam file and convert to bed format

.. code-block:: console

  samtools view -@24 -h -F 0x900 sampleA.bam | bedtools bamtobed -i stdin > sampleA.primary.aln.bed
  samtools view -@24 -h -F 0x900 sampleB.bam | bedtools bamtobed -i stdin > sampleB.primary.aln.bed

- 1.6 Call peaks

.. code-block:: console

  macs2 callpeak -t sampleA.primary.aln.bed -n sampleA --nomodel
  macs2 callpeak -t sampleB.primary.aln.bed -n sampleB --nomodel

2. Library Quality Control
--------------------------
**Question:** Are the data of good quality?

**Process:** Here we use the HiChIP QC scripts (available here: https://hichip.readthedocs.io/en/latest/library_qc.html) to assess the proximity-ligation and chromatin immunoprecipitation quality.  The QC process utilizes the pairtools stats file and a file of ChIP peaks for H3K27ac. In this example, ChIP-seq was not performed prior to the HiChIP. Therefore, the ENCODE file (encodeproject.org/files/ENCFF135ATY/) was used to assess enrichment observed vs. expected ratio. The command line-based steps used are denoted in steps 2.1 to 2.4. This step takes about 4 hours with deeply sequenced data sets (~200 million reads pairs).

**Results:** Both samples display similar high alignment (>80%) and acceptable duplication rates (< 30%) consistent with expectations of sufficiently complex HiChIP library, resulting in greater than 54% of the data as valid non duplicated pairs. Furthermore, the libraries show successful proximity-ligation and sufficient long-range interactions with more than 22% of the non-duplicated cis insert size were > 1kb (Figure 2A; Table 1). In the assessment of the IP-enrichment, we see that both libraries show a high concentration of reads at the peak centers with an observed:expected ratio of > 3 (Table 1), combined with the meta-data coverage plots at all H3K27ac in the ENCODE file (Figure 2B) indicate a successful IP. The IP scores may not perfectly reflect the experiment as the peak files were generated from a different experiment and do not reflect the conditions of the experimentally derived HiChIP libraries, but this is a suitable proxy to assess library quality. Both libraries pass the quality control thresholds, and we can proceed to further analyses. 

**Tools needed:**
  - :ref:`Scripts from the HiChIP Library QC Page. <LQ>`

**Commands:**

- 2.1 Get alignment and proximity-ligation QC stats from the pairtools stats file

.. code-block:: console

  python HiChIP/getqc.py -p sampleA.txt
  python HiChIP/getqc.py -p sampleB.txt

- 2.2 Download peaks file

.. code-block:: console

  wget https://www.encodeproject.org/files/ENCFF135ATY/@@download/ENCFF135ATY.bed.gz
  gunzip ENCFF135ATY.bed.gz

- 2.3 Get enrichment stats against encode file from the bam file (this takes a little while)

.. code-block:: console

  HiChIP/./enrichment_stats.sh -g mm10.genome -b sampleA.bam -p ENCFF135ATY.bed -t 16 -x sampleA.IP.txt
  HiChIP/./enrichment_stats.sh -g mm10.genome -b sampleB.bam -p ENCFF135ATY.bed -t 16 -x sampleB.IP.txt

- 2.4 Plot enrichment over the ENCODE Peaks file from the bam

.. code-block:: console

  python HiChIP/plot_chip_enrichment.py -bam Coverage_files/sampleA.bam -peaks ENCFF135ATY.bed -output sampleA.IP.png
  python HiChIP/plot_chip_enrichment.py -bam Coverage_files/sampleB.bam -peaks ENCFF135ATY.bed -output sampleB.IP.png

Table 1: HiChIP QC summary table.

.. image:: /images/Table1_QC_stats.png

Figure 2: HiChIP QC Results. A Alignment, PCR, and proximity ligation stats. Alignment stats are presented as a percentage of total read pairs. Proximity-ligation stats are presented as a percentage of No-Dup read pairs. B Chromatin IP efficiency, meta-peak analyses showing coverage as log fold change over the mean coverage across all encode peaks, and stats reporting the percent of No-dup reads over peaks and the observed/Expected ratio as summarized in Table 1.

.. image:: /images/Fig2_QC.png

3. Loop calling and differential looping
----------------------------------------

**Question:** Can differential HiChIP interactions be detected?

**Process:** To address this question we need to determine which interactions are significantly enriched within each condition, also known as loop calling, then determine which loops are unique to a condition or shared across conditions. The inputs are the  pairs files in HiC-Pro format (step 1.3) and the narrowPeak files generated in step (1.6). Then we run FitHiChIP, through Docker, and point to a configuration file. In this experiment loops will be identified at 5kb resolution, in a All-to-All manner, default loop ranges (20kb-2mb), coverage bias turned on, FitHiChIP(L) background modeling, and merging redundant loops. The configuration files are available in the directory you downloaded at the start of the workshop. Loop files will be extracted from the FitHiChIP output, NOTE- the output file has a “.bed” moniker but is actually in bedpe format. Using R, we’ll reformat the FitHiChIP output, then use bedtools pairToPair command with the “both” option flagged to identify loops between the two conditions that share the same anchor positions. Finally, we use the eulerr package in R to plot a Venn diagram. This process is outlined in the command steps 3.1 - 3.6. This process takes about 2 hours, most of which is on running FitHiChIP.

**Results:** Sample A (3,240 total loops) contains ~700 more loops than sample B (2,484 total loops). Of which 652 loops are shared between the two conditions, resulting in roughly 3,200 and 2,500 unique loops in sample A and sample B, respectively. These results are summarized in Figure 3.  

**Tools needed:**
  - FitHiChIP
  - bedtools
  - R
  
    - Packages: eulerr

**Commands:**

- 3.1 Call loops with FitHiChIP pointing the configuration file to the HiCPro format pairs generated in step #1.5

.. code-block:: console

  ./FitHiChIP_Docker.sh -C sampleA.config.file.txt
  ./FitHiChIP_Docker.sh -C sampleB.config.file.txt

- 3.2 Copy loop files to a into working directory from FitHiChIP output (these files are buried pretty deep in the FitHiChIP output)

.. code-block:: console

  cp sampleA_fit_out/FitHiChIP_ALL2ALL_b5000_L20000_U2000000/Coverage_Bias/FitHiC_BiasCorr/Merge_Nearby_Interactions/samplA_5kb.interactions_FitHiC_Q0.1_MergeNearContacts.bed .
  cp sampleB_fit_out/FitHiChIP_ALL2ALL_b5000_L20000_U2000000/Coverage_Bias/FitHiC_BiasCorr/Merge_Nearby_Interactions/samplB_5kb.interactions_FitHiC_Q0.1_MergeNearContacts.bed .

- 3.3 Clean files to and convert to bedpe format in R

.. code-block:: console

  # load libraries
  library(eulerr)
			
  # Import data
  lA <- read.table("sampleA_5kb.interactions_FitHiC_Q0.1_MergeNearContacts.bed", header=TRUE)
  lB <- read.table("sampleB_5kb.interactions_FitHiC_Q0.1_MergeNearContacts.bed", header=TRUE)
			
  # Add column for unique loop ID and binpair ID
  lA$LoopID <- paste("sampleA", seq_along(lA[,1]), sep="-")
  lB$LoopID <- paste("sampleB", seq_along(lB[,1]), sep="-")
  lA$Bin_Pair_ID <- paste(lA$chr1, lA$s1, lA$e1, lA$chr2, lA$s2, lA$e2, sep="-")
  lB$Bin_Pair_ID <- paste(lB$chr1, lB$s1, lB$e1, lB$chr2, lB$s2, lB$e2, sep="-")
			
  # Select desired columns
  lA.f <- subset(lA, select=c("chr1", "s1", "e1", "chr2", "s2", "e2", "cc", "LoopID"))
  lB.f <- subset(lB, select=c("chr1", "s1", "e1", "chr2", "s2", "e2", "cc", "LoopID"))
			
  # Print files as bedpe
  write.table(lA.f,"sampleA.clean.loops.bedpe",row.names=FALSE,sep="\t", col.names=FALSE, quote = FALSE)
  write.table(lB.f,"sampleB.clean.loops.bedpe",row.names=FALSE,sep="\t", col.names=FALSE, quote = FALSE)
			
  # Count number loops
  nrow(lA)
  nrow(lB)
			
  # Draw Venndiagram
  A = as.vector(lA$Bin_Pair_ID)
  B = as.vector(lB$Bin_Pair_ID)
  L=list(SampleA=A, Sample=B)
  L.plot <- plot(venn(L), fills = list(fill = c("blue", "red")), alpha=0.5)
  pdf("Loop_summary.pdf", height=10, width=10)
  L.plot
  dev.off()
			
  # Leave R
  q()

- 3.4 Use bedtools pairToPair to find shared loops and print bedpes

.. code-block:: console

  pairToPair -a sampleA.clean.loops.bedpe -b sampleB.clean.loops.bedpe -type both > overlapping_notclean.loops.bedpe

- 3.5 Cut columns into new files (one for plotting and one for filtering)

.. code-block:: console

  cut -f 1-6 overlapping_notclean.loops.bedpe > shared.clean.loops
  cut -f8,16 overlapping_notclean.loops.bedpe > shared.list.txt

- 3.6 Use R to make tables of shared and unique loops based on loop ID

.. code-block:: console

  # load libraries
  library(dplyr)
			
  # import data (clean loop tables and list of overlapping IDs)
  lA <- read.table("sampleA.clean.loops.bedpe", header=FALSE)
  lB <- read.table("sampleB.clean.loops.bedpe", header=FALSE)
  IDs <- read.table("shared.list.txt", header=FALSE)
			
  # rename columns
  lA <-  rename(lA,  chr1 = V1, s1 = V2, e1 = V3, chr2 = V4, s2 = V5, e2 =  V6, A_count = V7, sampleA_ID = V8)
  lB <-  rename(lB,  chr1 = V1, s1 = V2, e1 = V3, chr2 = V4, s2 = V5, e2 =  V6, B_count = V7, sampleB_ID = V8)
  IDs <-  rename(IDs,  sampleA_ID = V1, sampleB_ID = V2)
			
  # use anti join to get unique lists
  uA <- anti_join(lA, IDs, by="sampleA_ID")
  uB <- anti_join(lB, IDs, by="sampleB_ID")
			
  # select rows
  uA.f <- subset(uA, select=c("chr1", "s1", "e1", "chr2", "s2", "e2"))
  uB.f <- subset(uB, select=c("chr1", "s1", "e1", "chr2", "s2", "e2"))
			
  # print unique list
  write.table(uA.f,"unique.sampleA.loops.bedpe",row.names=FALSE,sep="\t", col.names=FALSE, quote = FALSE)
  write.table(uB.f,"unique.sampleB.loops.bedpe",row.names=FALSE,sep="\t", col.names=FALSE, quote = FALSE)
			
  # leave R
  q()

Figure 3. Summary of loop calls and differential looping. Venn diagram of overlapping produced in step 3.3.7, and slightly cleaned up in illustrator. The table of loop counts from running wc -l on the generated bedpe files.

.. image:: /images/Fig3_Differential_Looping.png

4. APA analysis to confirm loop analysis
----------------------------------------

**Question:** Do the contact matrices support the loop analysis?

**Process:** To check the results of the loop comparison we need to observe how to contact matrices behave at the shared and condition-specific unique loops. To do this, we need to average contact matrices at all loop sets (shared, unique A, and unique B) for both matrices. This is known as aggregate peak analysis (APA). Here we’ll used the bedpe’s generated in steps 3.5 and 3.6.6 as along with the contact matrices generated in step 1.6.2 in the tool coolpup.py to build the APA matrices, then plot with plotpup within the coolpup.py package. This approach not only generates matrices, but it also generates an APA score, which in the case of coolpup, is the Z-score of the mean contact density in the middle of the matrix to the mean of the entire matrix. Higher APA scores indicate stronger enrichment. This process is detailed in steps 4.1 - 4.2. This process takes about 15 mins.

**Results:** In general sample A shows a strong enrichment score at loops unique to sample A and shared loops, confirming that sample A has more loops than sample B. To understand if condition-specific loops are truly unique we ask how the contact matrix of the opposing sample behaves at unique loop sets. APA scores are strongest at their condition-specific loop calls, where in the other samples there is two-fold drop in contact enrichment. Moreover, there is a loss of a bright, punctate spot in the center of matrix. This suggests that while there is contact enrichment at loop sites in the opposing sample, they are significantly weaker. These finding posit that loops unique to a condition are truly unique. For loops that are shared across the conditions we see that APA scores are equivalent and display a strong contact signal in the center to the aggregated matrix, confirming that shared loops are, in fact, shared across the two conditions (Figure 4).

**Tools needed:**
  - coolpup.py

**Commands:**

- 4.1 Build aggregate contact signal over shared and unique loops with cool pup

.. code-block:: console

  coolpup.py sampleA.5kb.cool unique.sampleA.loops.bedpe --unbalanced --n_proc 24 --outname sAmatrix.vs.uAloops.txt
  coolpup.py sampleA.5kb.cool shared.clean.loops --unbalanced --n_proc 24 --outname sAmatrix.vs.sharedloops.txt
  coolpup.py sampleA.5kb.cool unique.sampleB.loops.bedpe --unbalanced --n_proc 24 --outname sAmatrix.vs.uBloops.txt
  coolpup.py sampleB.5kb.cool unique.sampleA.loops.bedpe --unbalanced --n_proc 24 --outname sBmatrix.vs.uAloops.txt
  coolpup.py sampleB.5kb.cool shared.clean.loops --unbalanced --n_proc 24 --outname sBmatrix.vs.sharedloops.txt
  coolpup.py sampleB.5kb.cool unique.sampleB.loops.bedpe --unbalanced --n_proc 24 --outname sBmatrix.vs.uBloops.txt


- 4.2 Plot aggregate contacts with plotpup

.. code-block:: console

  plotpup.py sAmatrix.vs.uAloops.txt sAmatrix.vs.sharedloops.txt sAmatrix.vs.uBloops.txt sBmatrix.vs.uAloops.txt sBmatrix.vs.sharedloops.txt sBmatrix.vs.uBloops.txt --row_names sampleA,sampleB --col_names unique_A,shared,unique_B --n_cols 3 --vmin 1 --vmax 100 --output loops.png

Figure 4. APA results. Aggregated matrices and APA score shown for all loop sets in both samples. Top row the sample A matrix is aggregated at sample A unique loops (left column), shared loops (center column), and sample B unique loops (right column). The same loops sets were used to aggregate the sample B matrix in the bottom row. APA scores (Z-scores) are shown in the top left of each APA matrix.

.. image:: /images/Fig4_APAs.png

5. Annotate and GO Enrichment Analysis
--------------------------------------

**Question:** What functions are enriched in those differential loops?

**Process:** Most annotation workflows use genomic ranges or bed file files to perform annotation. As loop files are in genomic interaction format or bedpe files they don’t directly plug into these analyses. To solve this - it is good think about the bedpe files as simply two bed entries of loop anchor positions side-by-side. With this understanding, we simply need to isolate the anchors in reach row into a separate bed files, merge, and sort to retain unique entries. This is quickly achieved with basic linux language, cut, cat, and sort. Now that we have our bed files of unique anchor position for each loop type, we can simply plug these data into an annotation package in R, such as ChIPseeker. Following the annotation, a Gene Ontology (GO) analyses can be performed to see which functions are enriched at loop anchors for each loop type. You can follow this workflow with steps 5.1 – 5.4. This process takes about 5 mins once all the packages are installed.

**Results:** Many of the functions that are enriched at loop anchors occur in both conditions. As our focus is the differences between sample A and sample B, we will not focus on the shared category. To this end, the functional differences can bed observed through the presence/absence of functions as in the GnRH signaling pathway and the Neurotrophin signaling pathway are present in sample A anchors, but not in sample B. More subtle change can be seen through the gene ratio (# of genes / total genes in loop anchors) such as Salmonella infection or Proteoglyancs in Cancer where sample A has more genes in the pathway associated with loop anchors. Differences in the significance of the enrichment also account for many of changes between sample A and sample B. There are numerous functions that fall into this last category, such as Heptocellular carcinoma, Gastric acid secretion, Growth hormone synthesis, secretion and action, and Glimoa (Figure 5). 

**Tools needed:**
  - R
  
    - Packages: ChIPseeker; TxDb.Mmusculus.UCSC.mm10.knownGene; EnsDb.Mmusculus.v79, clusterProfiler, AnnotationDbi, org.Mm.eg.db, dplyr

**Commands:**

- 5.1 Make bedfile of loop anchors

.. code-block:: console

  cut -f 1-3 unique.sampleA.loops.bedpe > sampleA.anchor1.bed
  cut -f 4-6 unique.sampleA.loops.bedpe > sampleA.anchor2.bed 
  cut -f 1-3 unique.sampleB.loops.bedpe > sampleB.anchor1.bed
  cut -f 4-6 unique.sampleB.loops.bedpe > sampleB.anchor2.bed
  cut -f 1-3 shared.loops.bedpe > shared.anchor1.bed
  cut -f 4-6 shared.loops.bedpe > shared.anchor2.bed 

- 5.2 cat anchor1 and anchor2 per loop condition and sort to retain unique entries

.. code-block:: console

  cat sampleA.anchor* | sort -u > sampleA.All.anchors.bed
  cat sampleB.anchor* | sort -u > sampleB.All.anchors.bed
  cat shared.anchor* | sort -u > shared.All.anchors.bed

- 5.3 move merged and sorted anchor beds into new directory called anchors

.. code-block:: console

  mkdir anchors
  mv *.All.* anchors/

- 5.4 Annotate in R and run GO enrichment analysis

.. code-block:: console

  # Load libraries
  library(ChIPseeker)
  library(TxDb.Mmusculus.UCSC.mm10.knownGene)
  ibrary(EnsDb.Mmusculus.v79)
  library(clusterProfiler)
  library(AnnotationDbi)
  library(org.Mm.eg.db)
  library(dplyr)
		
  # Import and organize anchor files
  samplefiles <- list.files("anchors/", pattern= ".bed", full.names=T)
  samplefiles <- as.list(samplefiles)
  names(samplefiles) <- c("sampleA", "sampleB", "shared")
			
  # Set reference database to annotate against
  txdb <- TxDb.Mmusculus.UCSC.mm10.knownGene
		
  # Annotate
  peakAnnoList <- lapply(samplefiles, annotatePeak, TxDb=txdb, tssRegion=c(-1000, 1000), verbose=FALSE)
		
  # GO analyses
  genes = lapply(peakAnnoList, function(i) as.data.frame(i)$geneId)
  compKEGG <- compareCluster(geneCluster = genes, fun="enrichKEGG", organism = "mouse", pvalueCutoff  = 0.05, pAdjustMethod = "BH")

  # Summarize GO in a dotplot
  p1 <- dotplot(compKEGG, showCategory = 20, title = "KEGG Pathway Enrichment Analysis")
  pdf("GO.pdf", height=15, width=8)
  p1
  dev.off()

  # Print GO analyses
  write.table(compKEGG, "KEGG_GO.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)

  # leave R
  q()

Figure 5. GO enrichment analysis results

.. image:: /images/Fig5_GO.png

6. Identify regions of interest through Pathway Analysis
--------------------------------------------------------

**Question:** Which genes within those functions should highlighted?

**Process:** In this step we will isolate the gene IDs that are present in both samples for the function we are interested in, and plot them on a KEGG pathway to see which genes have condition-specific loop anchors associated with them. To isolate the gene IDs, we’ll use the KEGG_GO.txt file generated 5.4.7 and select the function we’re interested in, in this case the Growth hormone synthesis, secretion and action (GHSSA). From there we perform a series of formatting steps to get the gene IDs into a vector format in R. In order to color the genes in the plot there needs to be a numeric value associated with each gene ID. As the data are currently in binary format (present/absent) we can apply a pseudo-log fold change, were absent equals 1 and present equal 20 to have a dramatic log fold change. Now we simply take the log of pseudo scores for gene IDs in sample A divided by the pseudo score for gene IDs in sample B. Next the gene IDs are merged with the pseudo-logFC score into a list format then plot the pathway of interest with pathview in R. This step takes ~5 mins.
 
**Results:** Through this approach we can easily identify which genes occur at loop anchors in sample A (red color), sample B (green color), or those with loop anchors in both samples (grey). This analysis indicates that the treatment leads to a general loss of looping associated with the GHSSA function with 15 gene showing in sample A loop anchors and only 5 gene showing enrichment in sample B loop anchors. One could interoperate this image as red gene boxes indicate a loss of looping during the treatment, where green gene boxes highlight gained loops, and grey are unchanged by the treatment (Figure 6).

**Tools needed:**
  - R
  
    - Packages: splitstackshape; data.table; dplyr; tidyr; pathview

**Commands:**

- 6.1 load libraries

.. code-block:: console

  library(splitstackshape)
  library(data.table)
  library(dplyr)
  library(tidyr)
  library(pathview)

- 6.2 import data

.. code-block:: console

  t <- read.table("KEGG_GO.txt", sep='\t', header=TRUE)

- 6.3 Select genes IDs in pathway of interest and format to get master list of IDs across sample A and B

.. code-block:: console

  t1 <- t[which(t$ID == "mmu04935"),]
  t2 <- select(t1, Cluster, geneID)
  row.names(t2) <- t2$Cluster
  t3 <- filter(t2, Cluster !="shared")
  ts <- cSplit(t3, "geneID", "/")
  tt <- transpose(ts)
  header.true <- function(tt) {names(tt) <- as.character(unlist(tt[1,]))
    tt[-1,]
    }
  tt1 <- header.true(tt)
  a <- select(tt1, sampleA)
  a<-rename(a, ID=sampleA)
  b <- select(tt1, sampleB)
  b<-rename(b, ID=sampleB)
  ml <- rbind(a,b)
  m <- unique(ml)
  m2 <- unique(ml)

- 6.4 build table of presence and absense in sample A and B

.. code-block:: console

  m$SampleA <- do.call(paste0, m) %in% do.call(paste0, a)
  m2$SampleB <- do.call(paste0, m2) %in% do.call(paste0, b)
  df <- merge (m, m2, by="ID")
  df <-df %>% drop_na()

- 6.5 change binary presence or absence into values to get a foldchange of presence or absence

.. code-block:: console

  df$sA.presence <- ifelse(df$SampleA=="TRUE", 20,1)
  df$sB.presence <- ifelse(df$SampleB=="TRUE", 20,1)
  df$logfc <- log(df$sA.presence/df$sB.presence)

- 6.6 make List of gene IDs and fold changes

.. code-block:: console

  d <- select(df, ID, logfc)
  mypathway <- "mmu04935"
  genes <- c(d$ID)
  logFC <- d$logfc
  names(logFC)<-genes

- 6.7 plot with pathview

.. code-block:: console

  pathview(gene.data=logFC,species="mmu",pathway=mypathway)

Figure 6. Differential gene enrichment at loop anchors in the Growth hormone synthesis, secretion and action (GHSSA) pathway. Red represents genes associated in sample A-specfic loop anchors, green are present only in sample loop anchors, and grey are present in both loop anchors. 

.. image:: /images/Fig6_KEGG_Path.png

7. Plotting regions of interest
-------------------------------

**Question:** How does looping at both conditions behave at those genes?

**Process:** All the previous work has lead to a point where we can now plot coverage signal showing H3K27ac enrichment and the significant interaction as arcs to understand how the treatment impacts a specific region. He we select the first gene in the pathway Ghrh, growth hormone releasing hormone which is a gained loop anchor. In order to inspect looping dynamics we plot the coverage, from the .bedgraph files generated in step 1.2 and the FitHiChIP loops generated in step 3.2 in in window 600kb window centered at the Ghrh promoter using the R package Sushi. This plotting excersie is captured in steps 7.1 – 7.2. This process takes about 15 mins.
 
**Results:** H3K27ac enrichment is almost identical between the two the two conditions. However, the looping dynamics are dramatically different. In this region, loops in sample B are more numerous, and stronger in contact strength (indicated by number of contacts). Specifically, Ghrh has a weak interaction with an H3K27ac enhancer ~130kb downstream at the SRC and 2819923M15Rik loci. This particular loop is absent in sample A. The resulting plot (Figure 7A) was cleaned up in the PDF editor Adobe Illustrator (Figure 7B).

**Tools needed:**
  - Adobe Illustrator or similar
  - R
  
    - Packages: sushi

**Commands:**

- 7.1 download and unzip refseq genes list in gtf format from UCSC

.. code-block:: console

  wget https://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/genes/mm10.refGene.gtf.gz
  gunzip mm10.refGene.gtf.gz

- 7.2 Plot results in R

.. code-block:: console

  # load libraries
  library(Sushi)
  library(dplyr)
  library(splitstackshape)

  # import coverage
    sA.covs <- read.table("sampleA.RPKM.bedgraph", header=F)
    sB.covs <- read.table("sampleB.RPKM.bedgraph", header=F)

  # import loops
    sA.arc <- read.table("sampleA_5kb.interactions_FitHiC_Q0.1_MergeNearContacts.bed", header=T)
    sB.arc <- read.table("sampleB_5kb.interactions_FitHiC_Q0.1_MergeNearContacts.bed", header=T)

  # import genes and format for sushi plotting
    g <- read.table("mm10.refGene.gtf", header=F, sep='\t')
    g2 <- cSplit(g, "V9", ";")
    g3 <- select(g2, V1, V2, V3, V4, V5, V6, V7, V8, V9_1)
    g4 <- cSplit(g3, "V9_1", " ")
    g5 <- select(g4, V1, V2, V3, V4, V5, V6, V7, V9_1_2)
    g5 <- rename(g5, "chrom"=V1, "source"=V2, "type"=V3, "start"=V4, "end"=V5, "score"=V6, "strand"=V7, "gene"=V9_1_2)
    trx <- g5[which(g5$type=='transcript'),]
    genes <- select(trx, chrom, start, end, gene, score, strand, type)

  #  Set ROI for GRGH
  chrom="chr2"
  chromstart=157238902
  chromend=157582101

  #  Plot ROI
  pdfname = "GRHRH.pdf"
  makepdf = TRUE

  if(makepdf == TRUE)
  {
    pdf(pdfname, height =5, width=10)
  }

  #set layout
  layout(matrix(c(1,1,1,1,
    2,2,2,2,
    3,3,3,3,
    4,4,4,4,
    5,5,5,5)
    , 5, 4, byrow=TRUE))

  # set margins
  par(mgp=c(0, 0.1, 0))

  # plot sampleA coverage
  par(mar=c(0.5,4,0.5,4))
  plotBedgraph(sA.covs, chrom, chromstart, chromend, color=SushiColors(2)(2)[1], ymax=1.5)
  axis(side=2,las=2,tcl=.2)
  mtext("Read Depth",side=2,line=1.75,cex=.5,font=2)
  legend("topright",inset=0,legend=c("Sample A","Sample B"),fill=SushiColors(2)(2), border=SushiColors(2)(2),text.font=2,cex=0.75)

  # plot sampleA FitHiChIP 5kb loops
  par(mar=c(0.5,4,0.5,4))
  plotBedpe(sA.arc, chrom, chromstart, chromend, heights = sA.arc$sumCC, plottype="loops", flip=TRUE, color=SushiColors(2)(2)[1], ymax=4)
  axis(side=2,las=2,tcl=.2)
  mtext("# Contacts",side=2,line=1.75,cex=.5,font=2)

  # plot sampleB coverage
  par(mar=c(0.5,4,0.5,4))
  plotBedgraph(sB.covs, chrom, chromstart, chromend, color=SushiColors(2)(2)[2], ymax=1.8)
  axis(side=2,las=2,tcl=.2)
  mtext("Read Depth",side=2,line=1.75,cex=0.5,font=2)

  # plot sampleB FitHiChIP 5kb loops
  par(mar=c(0.5,4,0.5,4))
  plotBedpe(sB.arc, chrom, chromstart, chromend, heights = sB.arc$sumCC, plottype="loops", flip=TRUE, color=SushiColors(2)(2)[2], ymax=1)
  axis(side=2,las=2,tcl=.2)
  mtext("# Contacts",side=2,line=1.75,cex=.5,font=2)

  # plot gene track
  par(mar=c(2,4,2,4))
  plotGenes(genes , chrom,chromstart,chromend, types=genes$type, maxrows=20,bheight=0.08,plotgenetype="box",bentline=TRUE,col="black", 						labeloffset=.5,fontsize=0.9,arrowlength = 0.2,labeltext=TRUE)
  labelgenome( chrom, chromstart,chromend,n=3,scale="Mb")

  # turn off plotter
  if(makepdf == TRUE)
  {
  dev.off()
  }

  # leave R
  q()

Figure 7. A) The output from plotting in Sushi. B) The image cleaned up in the pdf editor Adobe Illustrator

.. image:: /images/Fig7_ROI_track.png

Final thoughts and considerations
---------------------------------

**What if you don’t have paired ChIP-seq experiments?**
Best practices in HiChIP analyses is to have paired ChIP-seq experiments. This is because these approaches ask different molecular biology questions:

   - ChIP = Where is protein bound to DNA?
   - HiChIP = where is protein bound to DNA and what other loci are interacting with it?

This subtle difference means that HiChIP as enrichment signal falling outside of the target protein binding site. If there is no way to access ChIP data you can identify chromatin-IP peaks in the HiChIP libraries, but you must get over two issues

  - The long-range information in the sequence data breaks the assumption peak callers have about the structure of the paired-end read (they expect insert size of <1kb, where HiChIP has many PE reads with insert size >1kb)
  - The off-target enrichment associated with interacting loci looks like increase background noise to Peak Callers

To overcome the paired-end insert size assumption - we recommend to isolate the primary alignment from the bam and convert into bed format then feed into the peak caller. These results should be used with caution as there is still a background noise problem. Therefore, it is a good idea to filter these peaks to take only the top 75th percentile of the Q-scores to only take the “good peaks”.

**Commands:**

Get primary alignment from the bam file and convert to bed format

.. code-block:: console

  samtools view -@24 -h -F 0x900 sampleA.bam | bedtools bamtobed -i stdin > sampleA.primary.aln.bed
  samtools view -@24 -h -F 0x900 sampleB.bam | bedtools bamtobed -i stdin > sampleB.primary.aln.bed

Get primary alignment from the bam file and convert to bed format

.. code-block:: console

  macs2 callpeak -t sampleA.primary.aln.bed -n sampleA --nomodel
  macs2 callpeak -t sampleB.primary.aln.bed -n sampleB --nomodel

**Considerations:**

   - Replication – In this experiment biological replication is not used, but technical replication was used to minimize the number PCR duplicates and maximize the amount use-able data from the sequencer. If you use biological replicates, you should loop call independently on each replicate then you can apply the same differential looping analyses to identify a core-set of loops that are shared across all replicates within a condition then move on to differential looping between condition A and condition B 
   - Paired ChIP-seq experiments – As mentioned above, it is best practices to have paired ChIP-seq experiments. If that is not do-able, there are ways to work around it, you just need to be aware of the data structure and what the molecular biology is behind the sequence data you are using to call peaks.
   - Workflow efficiency – The walkthrough guide that accompanies this workshop is meant to be detailed breakdown of the step-by-step ‘recipe’ for how to work through HiChIP data. There are certainly ways to improve upon this or wrap part of this into little R scripts that perform many steps in one executable. Please feel free to do so!
   - What is your question – it is always good to keep your biological question in mind. This guide is meant to help address a set of questions that are commonly asked about loop analysis. There are, of course, many other questions one could ask of these data. Hopefully, this workshop empowers you to ask your own question now you’re comfortable with the data structure! 

