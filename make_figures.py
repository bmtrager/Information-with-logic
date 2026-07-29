#!/usr/bin/env python3
"""Regenerate the computed figures for the PNAS submission.

Each figure script is run with `src/` as the working directory (they resolve
their input data as "../data/..." and write their PNG into the CWD), then the
resulting PNG is moved into `figures/`.

Usage:
    python3 make_figures.py            # build all figures
    python3 make_figures.py results_a methods_a  # build a subset, by key
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
# Keys follow the panel each figure occupies in the submission:
#   results_a / results_b  -> Fig. \ref{fig:empirical_results}, panels (a) and (b)
#   methods_a / methods_b  -> Methods Fig. \ref{fig:tests}, panels (a) and (b)
FIGURES = {
    "results_a": ("bar_compress_5x7c_thresh.py", "compress_5x7c_thresh.png"),
    "results_b": (
        "no_need_to_know_hash5_thresh.py",
        "no_need_to_know_hash_5_thresh.png",
    ),
    "methods_a": ("plot2_count.py", "methods_targeted_queries.png"),
    "methods_b": (
        "alice_does_not_know_what_bob_knows.py",
        "methods_no_need_to_know.png",
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
