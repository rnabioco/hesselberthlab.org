---
title: People
type: landing

sections:
  - block: team-showcase
    id: people
    content:
      title: Lab Members
      # No user_groups: one continuous grid rather than a row per group, so a
      # single-person group like the PI does not get a row to itself. Roles are
      # shown on each card instead. `weight` puts the PI first, then staff,
      # then students.
      sort_by: weight
      sort_ascending: true
      # One group, so the block renders a single grid with no group heading of
      # its own — the heading only appears when more than one group is listed.
      # Naming the group also keeps people who are not current members, like
      # the Friends below, out of this grid.
      user_groups:
        - Lab
    design:
      max_columns: 4
      show_interests: false
      show_role: true
      show_social: true

  - block: team-showcase
    id: friends
    content:
      title: Friends of the Lab
      subtitle: Alumni and collaborators we work with.
      sort_by: weight
      sort_ascending: true
      user_groups:
        - Friends
    design:
      max_columns: 4
      show_interests: false
      show_role: true
      show_social: true
---
