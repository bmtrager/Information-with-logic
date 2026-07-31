# PNAS figure code

Code and input data that generate the four computed figures in the paper.

## Quick start

```bash
pip install -r requirements.txt
python3 make_figures.py
```

PNGs are written to `figures/`. To build a subset, pass figure keys:

```bash
python3 make_figures.py fig03a fig05a
```

This reads the precomputed summaries in `data/`. The raw test sets those
summaries came from are also included; re-deriving them is a separate step — see
[Regenerating the summaries](#regenerating-the-summaries).

## Figures

Four figures are generated, each rendered with matplotlib:

| Key | Output PNG | Paper figure |
| --- | --- | --- |
| `fig03a` | `fig03a_empirical_results_targeted_queries.png` | Fig. 3(a) — empirical results, targeted queries |
| `fig03b` | `fig03b_empirical_results_no_need_to_know.png` | Fig. 3(b) — empirical results, no need to know |
| `fig05a` | `fig05a_methods_targeted_queries.png` | Fig. 5(a) — methods, targeted queries |
| `fig05b` | `fig05b_methods_no_need_to_know.png` | Fig. 5(b) — methods, no need to know |

The paper's LaTeX embeds the `.pdf` version of each figure; the `.png` files are
the same plots in raster form.

## Layout

```
make_figures.py   driver: runs each plot script and collects its PNG
src/              plot scripts, encoder/analysis modules, and the summary drivers
data/             raw per-experiment test sets + the summary JSON derived from them
figures/          build output
```

### `src/`

Plot scripts, one per figure:

- `fig03a_empirical_results_targeted_queries.py` — relative compression vs. query kernel size
- `fig03b_empirical_results_no_need_to_know.py` — relative compression vs. receiver kernel size
- `fig05a_methods_targeted_queries.py` — targeted-query methods comparison
- `fig05b_methods_no_need_to_know.py` — "no need to know" methods comparison

Supporting modules imported by the above:

- `readjson.py` — loads the summary JSON and computes per-test-set aggregates
- `partition_encode.py` — partition encoder
- `enumerative.py` — enumerative source encoder
- `random_hash_encode.py` — random-hash / null-space encoder
- `random_encode_bernoulli.py` — Bernoulli random encoder
- `elias_delta.py` — Elias delta integer code
- `gf2elim.py` — GF(2) Gaussian elimination
- `tnf_baselines.py` — gzip/bz2/lzma baselines

Summary drivers — these rebuild `data/*_compressed_count.json` from the raw test
sets (see [Regenerating the summaries](#regenerating-the-summaries)):

- `run_compress.py` — processes all 12 test sets sequentially
- `run_compress_parallel.py` — same, one process per test set

### `data/`

Two files per experiment, for `p_s = 0.075`, `p_r = 0.5`, and the twelve values of
`p_q` the figures sample (24 files total):

- `test_set_<p_s>-<p_q>-<p_r>.json` — the raw test set (24-34 MB each, 369 MB
  total).
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

The plots do not need this step — run it only to re-derive the summaries from raw
data. Regeneration is deterministic: rebuilding a summary from its raw input
reproduces the committed file byte-for-byte.

## Requirements

Python 3 with numpy and matplotlib (see `requirements.txt`). Verified end to end
with Python 3.13.1, numpy 2.2.0, matplotlib 3.10.0.
