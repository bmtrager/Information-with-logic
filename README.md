# PNAS figure code

Python code and input data that reproduce the computed figures in the PNAS
submission (`content/paper-PNAS` in the `information-in-logic` repository).

## Quick start

```bash
pip install -r requirements.txt
python3 make_figures.py
```

PNGs are written to `figures/`. To build a subset, pass figure keys:

```bash
python3 make_figures.py results_a methods_a
```

## What reproduces

Four of the eight PNGs in `content/paper-PNAS` are matplotlib output and are
fully reproducible from this repository:

| Key | Output PNG | Appears as |
| --- | --- | --- |
| `results_a` | `compress_5x7c_thresh.png` | Fig. `empirical_results`, panel (a) |
| `results_b` | `no_need_to_know_hash_5_thresh.png` | Fig. `empirical_results`, panel (b) |
| `methods_a` | `methods_targeted_queries.png` | Methods Fig. `tests`, panel (a) |
| `methods_b` | `methods_no_need_to_know.png` | Methods Fig. `tests`, panel (b) |

Three of the four are byte-for-byte identical to the submitted PNGs when built
with matplotlib 3.10.0. `methods_targeted_queries.png` is visually identical but
not byte-identical: the submitted copy was rendered with matplotlib 3.9.4, and
the difference is confined to font rasterization and antialiasing (same image
dimensions, ~0.5% of pixels differing at glyph edges).

Note that the paper's LaTeX embeds the `.pdf` version of each figure; the `.png`
files are the same plots in raster form.

## What does not reproduce

The remaining four PNGs in `content/paper-PNAS` are **not** script output and no
code for them exists:

- `new_shannon_setup.png`
- `science_fig1.png`
- `science_fig2.png`
- `science_fig3.png`

These are hand-authored schematic diagrams (communication-model sketches, kernel
diagrams, and the end-to-end setup figure), saved as macOS screen captures —
their PNG metadata carries an `exif:UserComment` of `Screenshot`, whereas the
four generated figures carry a `Software: Matplotlib` tag. They must be edited
in their original drawing tool, not regenerated from here.

## Layout

```
make_figures.py   driver: runs each plot script and collects its PNG
src/              plot scripts and the encoder/analysis modules they import
data/             precomputed per-experiment summary JSON (inputs to the plots)
figures/          build output
```

### `src/`

Plot scripts, one per figure:

- `bar_compress_5x7c_thresh.py` — relative compression vs. query kernel size
- `no_need_to_know_hash5_thresh.py` — relative compression vs. receiver kernel size
- `plot2_count.py` — targeted-query methods comparison
- `alice_does_not_know_what_bob_knows.py` — "no need to know" methods comparison

Supporting modules imported by the above:

- `readjson.py` — loads the summary JSON and computes per-test-set aggregates
- `partition_encode.py` — partition encoder
- `enumerative.py` — enumerative source encoder
- `random_hash_encode.py` — random-hash / null-space encoder
- `random_encode_bernoulli.py` — Bernoulli random encoder
- `elias_delta.py` — Elias delta integer code
- `gf2elim.py` — GF(2) Gaussian elimination
- `compress_data_concat_new_nocnf.py` — gzip/bz2/lzma baselines

Also included for provenance: `run_compress.py` and `run_compress_parallel.py`,
the drivers that produced the `data/` summaries from the raw test sets.

### `data/`

Twelve `test_set_<p_s>-<p_q>-<p_r>_compressed_count.json` files — the summary
statistics the plots consume, at `p_s = 0.075`, `p_r = 0.5`, and the twelve
values of `p_q` the figures sample.

These are derived artifacts. The raw `test_set_*.json` inputs they were computed
from total ~2.7 GB and are not included here; they live in `experiments/data/` in
the `information-in-logic` repository. Regenerating a summary from raw data uses
`run_compress.py` (or `run_compress_parallel.py`), which expects the raw test
sets in `data/`.

## Requirements

Python 3 with numpy and matplotlib (see `requirements.txt`). Verified with
Python 3.13, numpy 2.2.0, matplotlib 3.10.0. Install matplotlib 3.9.4 to
reproduce `methods_targeted_queries.png` byte-for-byte.
