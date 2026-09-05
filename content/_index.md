---
title: ''
summary: ''
date: 2024-01-01
type: landing

design:
  spacing: '0'

sections:
  - block: markdown
    id: intro
    content:
      title: ''
      subtitle: ''
      text: |-
        <div class="wide lab-hero">
          <img class="lab-hero__mark" src="/media/lab-portrait.png" alt="The Hesselberth Lab" width="1018" height="522">
          <div class="lab-hero__body">
            <p class="eyebrow">RNA Technology &amp; Therapeutics · CU School of Medicine</p>
            <h1 class="lab-hero__title">Hesselberth Lab</h1>
            <p class="lab-hero__lede">A collaborative lab of RNA biologists, technology developers and data analysts, discovering and translating fundamental principles of RNA regulation — from how transfer RNA links the RNA and protein worlds, to RNA therapies built with clinicians at Children's Hospital Colorado.</p>
            <p class="lab-hero__actions">
              <a class="btn-gold" href="/publications/">Publications</a>
              <a class="btn-plain" href="/people/">Meet the lab</a>
              <a class="btn-plain" href="/software/">Software</a>
            </p>
            <p class="affil">
              <a href="https://medschool.cuanschutz.edu/rbi">RNA Bioscience Initiative</a> ·
              <a href="https://medschool.cuanschutz.edu/biochemistry">Biochemistry &amp; Molecular Genetics</a> ·
              <a href="https://www.cuanschutz.edu/">University of Colorado School of Medicine</a>
            </p>
          </div>
        </div>
    design:
      columns: '1'

  - block: markdown
    id: research
    content:
      title: ''
      text: |-
        <div class="wide">
          <p class="eyebrow">Research</p>
          <h2 class="section-title">What we study</h2>
          <div class="areas">
            <section>
              <h3><span class="n">01</span>RNA technology</h3>
              <p>We build sequencing methods and the software that makes sense of them: nanopore direct sequencing that reads modification and aminoacylation state on intact <span class="nocaps">tRNA</span>s, and single-cell and spatial approaches that measure biochemical activity alongside gene expression. Applied with collaborators, they track how antigen and viral <span class="nocaps">RNA</span> move through the lymph node.</p>
              <span class="with">Nanopore · Single-cell · Spatial · Open software</span>
            </section>
            <section>
              <h3><span class="n">02</span>RNA biology</h3>
              <p>Cells damage their own <span class="nocaps">RNA</span>, and repair it. We study how cleavage, end modification and processing are integrated into an <span class="nocaps">RNA</span> damage response, combining genetics, biochemistry and bioinformatics — work that has turned up new concepts in post-transcriptional regulation and, with collaborators, new determinants of nonsense-mediated decay.</p>
              <span class="with">RNA damage · Repair · <span class="nocaps">tRNA</span> · NMD</span>
            </section>
            <section>
              <h3><span class="n">03</span>RNA therapy</h3>
              <p>With clinicians at Children's Hospital Colorado we run a pipeline for antisense oligonucleotides that correct disease-causing splicing. The current focus is cryptic splicing — most recently an <span class="nocaps">ASO</span> that restores a ciliogenesis factor lost to a splicing mutation — alongside mRNA vaccine work with immunologists at CU Anschutz.</p>
              <span class="with">Antisense oligos · Cryptic splicing · Children's Hospital Colorado</span>
            </section>
          </div>
        </div>
    design:
      columns: '1'

  - block: collection
    id: papers
    content:
      title: Selected publications
      filters:
        folders:
          - publications
        featured_only: true
    design:
      view: citation-image

  - block: collection
    id: news
    content:
      title: Latest news
      page_type: blog
      count: 5
      filters:
        author: ''
        category: ''
        tag: ''
        exclude_featured: false
        exclude_future: false
        exclude_past: false
      offset: 0
      order: desc
    design:
      view: news-line

  - block: markdown
    id: labshot
    content:
      title: ''
      text: |-
        <div class="wide lab-shot">
          <img src="/media/lab-action.png" alt="Illustration of the Hesselberth Lab at work" width="1376" height="768">
        </div>
    design:
      columns: '1'
---
