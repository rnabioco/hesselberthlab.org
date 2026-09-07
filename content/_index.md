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
        {{< lab-hero >}}
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
