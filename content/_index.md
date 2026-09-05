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
            <h1 class="lab-hero__title">We build the tools, then <em>go where the biology is.</em></h1>
            <p class="lab-hero__lede">An RNA technology lab: nanopore, single-cell and spatial sequencing, and the analysis behind it, developed in-house and put to work with collaborators across CU Anschutz and beyond.</p>
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
              <h3><span class="n">01</span>Sequencing technology</h3>
              <p>We develop methods to read RNA directly: nanopore sequencing of intact tRNA, its modifications and its charging state, alongside single-cell and spatial approaches — and the analysis pipelines that make the signal interpretable.</p>
              <span class="with">Nanopore · Single-cell · Spatial</span>
            </section>
            <section>
              <h3><span class="n">02</span>Translation &amp; RNA decay</h3>
              <p>How transcripts are read and destroyed: tRNA modification and aminoacylation, the rules governing nonsense-mediated decay, and unusual translational events such as peptide-bond skipping.</p>
              <span class="with"><span class="nocaps">tRNA</span> · NMD · 2A peptides</span>
            </section>
            <section>
              <h3><span class="n">03</span>RNA therapeutics</h3>
              <p>Splice-switching antisense oligonucleotides for pediatric genetic disease, developed with clinicians at Children's Hospital Colorado — and applied with immunologists, virologists and cell biologists wherever the methods are useful.</p>
              <span class="with">Children's Hospital Colorado</span>
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
