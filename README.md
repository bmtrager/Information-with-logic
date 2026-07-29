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

This reads the precomputed summaries in `data/` and takes about 2 seconds. The
raw test sets those summaries came from are also included; re-deriving them is a
separate, much slower step — see [Regenerating the summaries](#regenerating-the-summaries).

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
not byte-identical, and pinning a matplotlib version does not change that: the
submitted copy carries a matplotlib 3.9.4 tag, but building under 3.9.4 yields a
third distinct hash while leaving the pixel difference unchanged, so the
matplotlib version is not the cause. The residual difference is sub-pixel
rendering jitter — same image dimensions (1516x1815), ~0.59% of pixels differing,
spread over both glyph edges and the plotted curves/markers. It is cosmetic
rather than a data difference: per-color pixel counts match to within 16 px of
~2200 and mark centroids shift by only ~1-3 px out of 1815. The most likely
remaining variable is the host font stack (the submitted PNG was rendered on a
different machine); reproducing it exactly is not expected.

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
src/              plot scripts, encoder/analysis modules, and the summary drivers
data/             raw per-experiment test sets + the summary JSON derived from them
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

Summary drivers — these rebuild `data/*_compressed_count.json` from the raw test
sets (see [Regenerating the summaries](#regenerating-the-summaries)):

- `run_compress.py` — processes all 12 test sets sequentially
- `run_compress_parallel.py` — same, one process per test set

### `data/`

Two files per experiment, for `p_s = 0.075`, `p_r = 0.5`, and the twelve values of
`p_q` the figures sample (24 files total):

- `test_set_<p_s>-<p_q>-<p_r>.json` — the raw test set (24-34 MB each, 369 MB
  total). Copied from `experiments/data/` in the `information-in-logic`
  repository and verified identical by checksum.
- `test_set_<p_s>-<p_q>-<p_r>_compressed_count.json` — the summary statistics the
  plot scripts actually consume, derived from the raw set above.

Both levels are committed, so the chain from raw data to figure is reproducible
end to end.

#### Regenerating the summaries

```bash
cd src
python3 run_compress_parallel.py    # all 12, one process each
python3 run_compress.py             # all 12, sequentially
```

Both drivers glob `../data/*0.5.json` and write each
`<name>_compressed_count.json` **next to its input, overwriting in place**. Back
up `data/*_compressed_count.json` first if you want to compare before/after.

This step is far slower than plotting: about 7 minutes per file single-threaded
(~1.5 h for all 12 sequentially; roughly the cost of the slowest file when run in
parallel), against ~2 seconds for all four figures. The plots do not need it —
run it only to re-derive the summaries from raw data.

Verified deterministic: regenerating
`test_set_0.075-0.125-0.5_compressed_count.json` from its raw input reproduces
the committed summary byte-for-byte.

## Requirements

Python 3 with numpy and matplotlib (see `requirements.txt`). Verified end-to-end
with Python 3.13.1, numpy 2.2.0, matplotlib 3.10.0: all four figures build in
about 2 seconds, and three are byte-identical to the submitted PNGs. Under this
configuration `methods_targeted_queries.png` differs cosmetically only (see
"What reproduces" above); no dependency pin is known to make it byte-identical.
