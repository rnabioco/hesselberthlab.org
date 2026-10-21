"""Copy rendered publication illustrations into their page bundles.

Reads graphics/out/cu/pubs-rest/<slug>.png and writes
content/publications/<slug>/featured.png, also covering preprint/published
twins that share one illustration.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "graphics/out/cu/pubs-rest"
PUBS = ROOT / "content/publications"

TWINS = {
    "garrey-2014-ow": ["garrey-2014-zn"],
    "kosmaczewski-2014-hd": ["kosmaczewski-2014-ff"],
    "la-count-2005-my": ["la-count-2005-mz"],
    "peach-2015-vy": ["peach-2015-wy"],
    "robertson-2001-cm": ["robertson-2001-ya"],
    "schutz-2010-ha": ["schutz-2010-wt"],
    "tuttle-2018-fn": ["tuttle-2018-jb"],
    "gillen-2020-jl": ["gillen-2019-gp"],
    "koh-2015-oe": ["koh-2019-df"],
    "bryan-2014-ae": ["ransom-2018-rm"],
}

for png in sorted(SRC.glob("*.png")):
    for slug in [png.stem, *TWINS.get(png.stem, [])]:
        dest = PUBS / slug
        if dest.is_dir():
            shutil.copyfile(png, dest / "featured.png")
            print("installed", slug)
