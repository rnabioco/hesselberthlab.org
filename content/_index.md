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
          <img class="lab-hero__mark" src="/media/hesselberth-lab-hex-logo.jpg" alt="Hesselberth Lab">
          <div class="lab-hero__body">
            <p class="eyebrow">RNA Biology &amp; Therapeutics · CU School of Medicine</p>
            <h1 class="lab-hero__title">Reading translation, <em>one tRNA at a time.</em></h1>
            <p class="lab-hero__lede">We are RNA biologists, technology developers and data analysts working out how transfer RNA shapes protein synthesis — and turning what we learn into RNA therapies.</p>
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
              <h3><span class="n">01</span>tRNA &amp; translation</h3>
              <p>Transfer RNAs link the RNA and protein worlds. We apply nanopore sequencing to read tRNA sequence, modification and aminoacylation state on single molecules, resolving how tRNA is used across the steps of protein synthesis.</p>
              <span class="with">Nanopore · aa-tRNA-seq</span>
            </section>
            <section>
              <h3><span class="n">02</span>RNA therapeutics</h3>
              <p>We work with clinicians at Children's Hospital Colorado to develop RNA therapies for pediatric genetic disease, lately focused on inherited retinopathies and on correcting cryptic splicing.</p>
              <span class="with">Children's Hospital Colorado</span>
            </section>
            <section>
              <h3><span class="n">03</span>Immunity &amp; infection</h3>
              <p>With immunologists and virologists we develop new ways to manipulate and understand the mammalian immune system, from antigen archiving to how viruses persist in tissue.</p>
              <span class="with">Collaborative studies</span>
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
      view: citation

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
      view: date-title-summary
---
