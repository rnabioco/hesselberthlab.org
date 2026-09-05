---
title: 'scraps: an end-to-end pipeline for measuring alternative polyadenylation at
  high resolution using single-cell RNA-seq'
authors:
- Rui Fu
- Kent A Riemondy
- ryan-sheridan
- jay-hesselberth
- Craig T Jordan
- Austin E Gillen
date: '2022-08-01'
publishDate: '2026-02-13T13:27:51.433563Z'
publication_types:
- manuscript
publication:
  name: bioRxiv
  pages: 2022.08.22.504859
abstract: "Alternative cleavage and polyadenylation (APA) contributes to the diversity
  of mRNA 3' ends, affecting post-transcriptional regulation by including or excluding
  cis -regulatory elements in mRNAs, altering their stability and translational efficiency.
  While APA analysis has been applied broadly in mixed populations of cells, the heterogeneity
  of APA among single cells has only recently begun to be explored. We developed an
  approach we termed scraps (Single Cell RNA PolyA Site Discovery), implemented as
  a user-friendly, scalable, and reproducible end-to-end workflow, to identify polyadenylation
  sites at near-nucleotide resolution in single cells using 10X Genomics and other
  TVN-primed single-cell RNA-seq (scRNA-seq) libraries. Our approach, which performs
  best with long (>100bp) read 1 sequencing and paired alignment to the genome, is
  both unbiased relative to existing methods that utilize only read 2 and recovers
  more sites at higher resolution, despite the reduction in read quality observed
  on most modern DNA sequencers following homopolymer stretches. For libraries sequenced
  without long read 1, we implement a fallback approach using read 2-only alignments
  that performs similarly to our optimal approach, but recovers far fewer polyadenylation
  sites per experiment. scraps also enables assessment of internal priming capture
  events, which we demonstrate occur commonly but at higher frequency during apoptotic
  3' RNA decay. We also provide an R package, scrapR, that integrates the results
  of the scaps pipeline with the popular Seruat single-cell analysis package. Refinement
  and expanded application of these approaches will further clarify the role of APA
  in single cells, as well as the effects of internal priming on expression measurements
  in scRNA-seq libraries. ### Competing Interest Statement The authors have declared
  no competing interest."
hugoblox:
  ids:
    doi: 10.1101/2022.08.22.504859
---
