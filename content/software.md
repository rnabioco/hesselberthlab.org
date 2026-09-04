---
title: Software
type: landing

# Star counts and the pinned set were read from the GitHub API:
#   gh api graphql -f query='{organization(login:"rnabioco"){
#     pinnedItems(first:12,types:REPOSITORY){nodes{... on Repository{
#       name stargazerCount primaryLanguage{name} description}}}}}'
#   gh api "orgs/rnabioco/repos?per_page=100&sort=updated"
# They are a snapshot, not live — refresh them when they drift.

sections:
  - block: markdown
    id: software
    content:
      title: ''
      text: |-
        <div class="wide">
          <p class="eyebrow">Open source</p>
          <h2 class="section-title">Software</h2>
          <p class="sw-lede">We build and maintain open-source tools for RNA biology, nanopore sequencing and single-cell analysis. Everything lives in the <a href="https://github.com/rnabioco">rnabioco</a> organisation on GitHub.</p>

          <p class="eyebrow eyebrow--bare">Pinned on GitHub</p>
          <div class="sw-grid">
            <a class="sw-card" href="https://github.com/rnabioco/sracha-rs">
              <span class="sw-name">sracha-rs</span>
              <span class="sw-desc">Rust-based sra-tools.</span>
              <span class="sw-meta"><span class="sw-lang">Rust</span><span class="sw-stars">72</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/escapepod-rs">
              <span class="sw-name">escapepod-rs</span>
              <span class="sw-desc">Rust library and CLI for reading and writing ONT pod5 files.</span>
              <span class="sw-meta"><span class="sw-lang">Rust</span><span class="sw-stars">3</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/clover">
              <span class="sw-name">clover</span>
              <span class="sw-desc">Analysis of nanopore tRNA sequencing data.</span>
              <span class="sw-meta"><span class="sw-lang">R</span><span class="sw-stars">2</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/squiggy-positron">
              <span class="sw-name">squiggy-positron</span>
              <span class="sw-desc">Positron extension for visualising POD5 nanopore signals.</span>
              <span class="sw-meta"><span class="sw-lang">Python</span><span class="sw-stars">2</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/leech">
              <span class="sw-name">leech</span>
              <span class="sw-desc">Learning enhanced electrical classifiers from nanopore signals.</span>
              <span class="sw-meta"><span class="sw-lang">Python</span><span class="sw-stars">0</span></span>
            </a>
          </div>

          <p class="eyebrow eyebrow--bare">RNA &amp; single-cell analysis</p>
          <div class="sw-grid">
            <a class="sw-card" href="https://github.com/rnabioco/clustifyr">
              <span class="sw-name">clustifyr</span>
              <span class="sw-desc">Infer cell types in scRNA-seq data using bulk RNA-seq or gene sets.</span>
              <span class="sw-meta"><span class="sw-lang">R</span><span class="sw-stars">127</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/valr">
              <span class="sw-name">valr</span>
              <span class="sw-desc">Genome interval arithmetic in R, with a tidy interface.</span>
              <span class="sw-meta"><span class="sw-lang">R</span><span class="sw-stars">97</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/djvdj">
              <span class="sw-name">djvdj</span>
              <span class="sw-desc">Analyse single-cell V(D)J data.</span>
              <span class="sw-meta"><span class="sw-lang">R</span><span class="sw-stars">30</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/ggtrace">
              <span class="sw-name">ggtrace</span>
              <span class="sw-desc">ggplot2 geoms to outline groups of data points.</span>
              <span class="sw-meta"><span class="sw-lang">R</span><span class="sw-stars">16</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/scraps">
              <span class="sw-name">scraps</span>
              <span class="sw-desc">Single-cell RNA poly(A) site discovery.</span>
              <span class="sw-meta"><span class="sw-lang">Python</span><span class="sw-stars">11</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/raer">
              <span class="sw-name">raer</span>
              <span class="sw-desc">Characterise A-to-I RNA editing in bulk and single-cell RNA-seq.</span>
              <span class="sw-meta"><span class="sw-lang">C</span><span class="sw-stars">10</span></span>
            </a>
          </div>

          <p class="eyebrow eyebrow--bare">Nanopore sequencing</p>
          <div class="sw-grid">
            <a class="sw-card" href="https://github.com/rnabioco/tRNA004">
              <span class="sw-name">tRNA004</span>
              <span class="sw-desc">Direct tRNA sequencing method refinement and modification basecalling.</span>
              <span class="sw-meta"><span class="sw-lang">Python</span><span class="sw-stars">8</span></span>
            </a>
          </div>

          <p class="eyebrow eyebrow--bare">Infrastructure &amp; teaching</p>
          <div class="sw-grid">
            <a class="sw-card" href="https://github.com/rnabioco/nihexporter">
              <span class="sw-name">nihexporter</span>
              <span class="sw-desc">An R data package for NIH EXPORTER grant data.</span>
              <span class="sw-meta"><span class="sw-lang">R</span><span class="sw-stars">15</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/cpp11bigwig">
              <span class="sw-name">cpp11bigwig</span>
              <span class="sw-desc">Read bigWig and bigBed files in R.</span>
              <span class="sw-meta"><span class="sw-lang">C</span><span class="sw-stars">4</span></span>
            </a>
            <a class="sw-card" href="https://github.com/rnabioco/molb-7950">
              <span class="sw-name">MOLB 7950</span>
              <span class="sw-desc">Informatics and statistics for molecular biology — course materials.</span>
              <span class="sw-meta"><span class="sw-lang">Course</span><span class="sw-stars">5</span></span>
            </a>
          </div>
        </div>
    design:
      columns: '1'
---
