---
title: ''
summary: ''
date: 2024-01-01
type: landing

design:
  spacing: '1.5rem'

sections:
  - block: markdown
    content:
      title: ''
      subtitle: ''
      text: |-
        <div style="text-align: center; margin-bottom: 2rem;">
          <img src="/media/hesselberth-lab-hex-logo.jpg" alt="Hesselberth Lab" style="max-width: 200px; border-radius: 12px;" />
        </div>

        **Our Mission.** We are a collaborative research laboratory comprising RNA biologists, technology developers, and data analysts focused on discovering and translating fundamental principles of RNA regulation.

        **Core Research.** Our major focus in the lab is to understand protein translation through the lens of transfer RNA (tRNA). Transfer RNAs link the RNA and protein worlds, and our newest approaches apply nanopore sequencing technologies to understand the dynamic use of tRNA across multiple steps in protein translation.

        **Clinical Applications.** Our newest efforts focus on RNA therapeutics. We work with clinicians at Children's Hospital Colorado to develop RNA therapies for pediatric genetic diseases (lately focused on retinopathies), and with immunologists and virologists to develop new ways to manipulate and understand the mammalian immune system.

        *See our [publications](/publications/) for more detail on these studies.*

        ---

        *Our affiliations:*
        [RNA Bioscience Initiative](https://medschool.cuanschutz.edu/rbi) ·
        [Biochemistry & Molecular Genetics](https://medschool.cuanschutz.edu/biochemistry) ·
        [University of Colorado School of Medicine](https://www.cuanschutz.edu/)
    design:
      columns: '1'

  - block: collection
    id: papers
    content:
      title: Featured Publications
      filters:
        folders:
          - publications
        featured_only: true
    design:
      view: article-grid
      columns: 2

  - block: collection
    id: news
    content:
      title: Recent News
      subtitle: ''
      text: ''
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
      view: card
      spacing:
        padding: [0, 0, 0, 0]
---
