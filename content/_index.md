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
            <h1 class="lab-hero__title">How cells read, use <em>and destroy RNA.</em></h1>
            <p class="lab-hero__lede">Every transcript carries more than its sequence — modifications, charging state, structure — and cells act on all of it. We build the sequencing methods that make those features visible, and follow them into translation, immunity and disease.</p>
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
              <h3><span class="n">01</span>Reading RNA directly</h3>
              <p>Standard sequencing averages away most of what a transcript carries. We develop nanopore methods that keep it — chemical modifications, aminoacylation state, whole intact molecules — alongside single-cell and spatial approaches, and the analysis that makes the signal interpretable.</p>
              <span class="with">Nanopore · Single-cell · Spatial</span>
            </section>
            <section>
              <h3><span class="n">02</span>Translation &amp; RNA decay</h3>
              <p>What determines whether a transcript is translated, mistranslated or destroyed: the rules governing nonsense-mediated decay, unusual translational events such as peptide-bond skipping, and the modified <span class="nocaps">tRNA</span>s that supply the ribosome.</p>
              <span class="with">NMD · 2A peptides · <span class="nocaps">tRNA</span></span>
            </section>
            <section>
              <h3><span class="n">03</span>RNA therapeutics</h3>
              <p>Turning that understanding into treatment: splice-switching antisense oligonucleotides that correct cryptic exon inclusion in pediatric genetic disease, developed with clinicians at Children's Hospital Colorado.</p>
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
