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
            {{< research-areas >}}
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
      # Sized to the publication list beside it: five items left about 360px of
      # the column empty, which is roughly five more of these lines.
      count: 10
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
