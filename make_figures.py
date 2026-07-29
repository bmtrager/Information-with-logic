#!/usr/bin/env python3
"""Regenerate the computed figures.

Each figure script is run with `src/` as the working directory (they resolve
their input data as "../data/..." and write their PNG into the CWD), then the
resulting PNG is moved into `figures/`.

Usage:
    python3 make_figures.py            # build all figures
    python3 make_figures.py fig03a fig05a  # build a subset, by key
"""

import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "figures")

# key -> (script in src/, PNG the script writes)
#
# Keys are the figure labels used in the paper:
#   fig03a / fig03b  -> Fig. 3, panels (a) and (b): empirical results
#   fig05a / fig05b  -> Fig. 5, panels (a) and (b): methods
FIGURES = {
    "fig03a": (
        "fig03a_empirical_results_targeted_queries.py",
        "fig03a_empirical_results_targeted_queries.png",
    ),
    "fig03b": (
        "fig03b_empirical_results_no_need_to_know.py",
        "fig03b_empirical_results_no_need_to_know.png",
    ),
    "fig05a": (
        "fig05a_methods_targeted_queries.py",
        "fig05a_methods_targeted_queries.png",
    ),
    "fig05b": (
        "fig05b_methods_no_need_to_know.py",
        "fig05b_methods_no_need_to_know.png",
    ),
}


def build(key):
    script, png = FIGURES[key]
    print(f"[{key}] running src/{script} ...")
    subprocess.run([sys.executable, script], cwd=SRC, check=True)
    os.makedirs(OUT, exist_ok=True)
    shutil.move(os.path.join(SRC, png), os.path.join(OUT, png))
    print(f"[{key}] wrote figures/{png}")


def main(argv):
    keys = argv[1:] or list(FIGURES)
    unknown = [k for k in keys if k not in FIGURES]
    if unknown:
        sys.exit(f"unknown figure key(s): {', '.join(unknown)}\n"
                 f"available: {', '.join(FIGURES)}")
    for key in keys:
        build(key)
    print(f"\nDone. {len(keys)} figure(s) in figures/")


if __name__ == "__main__":
    main(sys.argv)
