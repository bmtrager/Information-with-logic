# Figure code and input data for "Fundamental limits incorporating logical reasoning into Shannon's information theory"

Accompanies the paper by L. A. Lastras, J. Lenchner, B. M. Trager, W.
Szpankowski, M. S. Squillante, C. W. Wu, R. Fagin, and A. Gray, *Proceedings of
the National Academy of Sciences* (2026). This repository generates the four
computed figures. See [Citation](#citation) below.

## Quick start

```bash
pip install -r requirements.txt
python3 make_figures.py
```

Vector PDFs are written to `figures/`. To build a subset, pass figure keys:

```bash
python3 make_figures.py fig03a fig05a
```

This reads the precomputed summaries in `data/`. The raw test sets those
summaries came from are also included, as is the code that generated them, so
the full chain is rebuildable — see
[Regenerating the summaries](#regenerating-the-summaries) and
[Regenerating the raw test sets](#regenerating-the-raw-test-sets).

## Figures

Four figures are generated, each rendered with matplotlib:

| Key | Output PDF | Paper figure |
| --- | --- | --- |
| `fig03a` | `fig03a_empirical_results_targeted_queries.pdf` | Fig. 3(a) — empirical results, targeted queries |
| `fig03b` | `fig03b_empirical_results_no_need_to_know.pdf` | Fig. 3(b) — empirical results, no need to know |
| `fig05a` | `fig05a_methods_targeted_queries.pdf` | Fig. 5(a) — methods, targeted queries |
| `fig05b` | `fig05b_methods_no_need_to_know.pdf` | Fig. 5(b) — methods, no need to know |

The paper's LaTeX embeds this same `.pdf` file directly (vector graphics, no
rasterization).

## Layout

```
make_figures.py   driver: runs each plot script and collects its PDF
src/              plot scripts, encoder/analysis modules, and the drivers that
                  regenerate the summaries and the raw test sets
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

Test-set generation — this builds the raw `data/test_set_*.json` from scratch
(see [Regenerating the raw test sets](#regenerating-the-raw-test-sets)):

- `main_tnf_json.py` — driver: emits the JSON summarizing the TNF, CNF, and zero
  sets for each test set

Supporting modules imported by the generator:

- `truthSet.py` — a truth set (class `TruthSet`): the set of truth-value
  assignments to the underlying variables assumed to make a given CNF or TNF
  true
- `query.py` — a query the receiver must be able to answer (class `Query`), a
  `TruthSet` with a couple of special properties
- `clause.py` — a CNF clause (class `Clause`)
- `cnf.py` — generating and working with a Boolean CNF (Conjunctive Normal Form)
  formula from a truth set (class `CNF`)
- `tnf.py` — generating and working with a custom TNF (Tree Normal Form) formula
  from a truth set (class `TNF`). Given a truth set, a most-bifurcating variable
  `X_v` is found and the TNF is rendered as
  `(X_v ^ TNF_0) v (-X_v ^ TNF'_0)`, where `TNF_0` and `TNF'_0` are TNFs over
  the same variables with `X_v` removed. TNFs can generally be rendered somewhat
  more efficiently than CNFs.
- `parser.py` — general-purpose parsing for CNF and TNF, including transforming
  either into postfix form for compressed representation (classes `Parser` and
  its helper `Block`)

### `data/`

Two files per experiment, for `p_s = 0.075`, `p_r = 0.5`, and the twelve values of
`p_q` the figures sample (24 files total):

- `test_set_<p_s>-<p_q>-<p_r>.json` — the raw test set (24-34 MB each, 369 MB
  total).
- `test_set_<p_s>-<p_q>-<p_r>_compressed_count.json` — the summary statistics the
  plot scripts actually consume, derived from the raw set above.

Both levels are committed, so the chain from raw data to figure is reproducible
end to end. The generator that produced the raw sets is committed too, under
`src/` — see [Regenerating the raw test sets](#regenerating-the-raw-test-sets).

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

#### Regenerating the raw test sets

`src/main_tnf_json.py` generates the raw `test_set_*.json` from scratch. With no
arguments it emits both TNF and CNF:

```bash
cd src
python3 main_tnf_json.py
```

A single argument selects which normal forms to emit: `-c` for CNF only, `-t` for
TNF only. The following are all equivalent to passing nothing (both forms):

```bash
python3 main_tnf_json.py
python3 main_tnf_json.py -ct
python3 main_tnf_json.py -tc
```

The committed test sets in `data/` contain **only** TNF, and are regenerated
with:

```bash
python3 main_tnf_json.py -t
```

Each run writes twelve `test_set_<p_s>-<p_q>-<p_r>.json` files **into the current
working directory** — so the command above leaves them in `src/`, not `data/`.
Move them into `data/` to have the summary drivers and plots pick them up, and
back up the committed copies first if you want to compare.

The parameters are constants at the top of `main_tnf_json.py`: `NUM_VARS = 10`
variables, `NUM_TEST_CASES = 1000` test cases per set, and the `p_s`/`p_q`/`p_r`
lists giving the twelve `(0.075, p_q, 0.5)` combinations the figures sample.

Unlike the summary step, this step is **not** reproducible byte-for-byte: the
test cases are drawn from an unseeded `random`, so each run produces a fresh
sample. Re-deriving summaries from newly generated test sets will therefore shift
the figures within sampling noise rather than reproduce them exactly. Use the
committed test sets to reproduce the published figures.

## Requirements

Python 3 with numpy and matplotlib (see `requirements.txt`). Verified end to end
with Python 3.13.1, numpy 2.2.0, matplotlib 3.10.0.

## Citation

If you use this code, please cite the accompanying paper:

> L. A. Lastras, J. Lenchner, B. M. Trager, W. Szpankowski, M. S. Squillante,
> C. W. Wu, R. Fagin, and A. Gray, "Fundamental limits incorporating logical
> reasoning into Shannon's information theory," *Proceedings of the National
> Academy of Sciences*, 2026. DOI: _to be added_.

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff); the DOI will be
filled in there once assigned.
