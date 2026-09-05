---
title: News
cms_exclude: true

view: news-line

# Each item is a single sentence, so a page per item would be a page holding
# one line. `_target.kind: page` applies this to the items only, not to this
# section index: they emit no page of their own, but still list everywhere, so
# the homepage can pull the five most recent.
cascade:
  - _target:
      kind: page
    _build:
      render: never
      list: always

banner:
  caption: ''
  image: ''
---
