#!/usr/bin/env Rscript
# Composite the generated lab portraits into a family portrait for the homepage.
#
#   pixi run -e graphics portrait
#
# Reads assets/media/authors/<slug>.png — the same avatars the People page
# uses — so the composite always matches the roster. Writes two layouts to
# graphics/out/; the block one is copied to static/media/lab-portrait.png.
#
# Order matches the People page: PI, then staff, then students.
library(magick)

slugs <- c("jay-hesselberth", "erika-lasda", "ryan-sheridan", "kezia-dobson",
           "grace-li", "jill-bilodeaux", "emily-decurtis", "ira-fleming")
CREAM <- "#FAF7F0"

# A circular crop. image_composite(..., "copyopacity") is the operator that
# actually works here: "In" and "DstIn" both return an opaque black corner.
circle <- function(slug, d) {
  img <- image_resize(
    image_read(file.path("assets/media/authors", paste0(slug, ".png"))),
    paste0(d, "x", d, "!"))
  m <- image_draw(image_blank(d, d, "none"))
  symbols(d / 2, d / 2, circles = d / 2 - 1, inches = FALSE, add = TRUE,
          bg = "white", fg = NA)
  dev.off()
  image_composite(img, m, operator = "copyopacity")
}

# Overlapping row — a wide banner.
d <- 260; ov <- 58
cs <- lapply(slugs, circle, d = d)
band <- image_blank(d * length(cs) - ov * (length(cs) - 1), d, CREAM)
for (i in seq_along(cs))
  band <- image_composite(band, cs[[i]], offset = geometry_point((i - 1) * (d - ov), 0))
image_write(image_border(band, CREAM, "26x26"), "graphics/out/lab-portrait-row.png", format = "png")

# 4 x 2 block — compact enough to sit beside the hero text.
d2 <- 230; gap <- 18
cs2 <- lapply(slugs, circle, d = d2)
blk <- image_blank(4 * d2 + 3 * gap, 2 * d2 + gap, CREAM)
for (i in seq_along(cs2)) {
  r <- (i - 1) %/% 4; c <- (i - 1) %% 4
  blk <- image_composite(blk, cs2[[i]], offset = geometry_point(c * (d2 + gap), r * (d2 + gap)))
}
image_write(image_border(blk, CREAM, "22x22"), "graphics/out/lab-portrait-block.png", format = "png")

cat("wrote graphics/out/lab-portrait-{row,block}.png\n")
