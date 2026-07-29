"""Regenerate every ``*_compressed_count.json`` summary, one test set at a time.

Run from the ``src`` directory: ``python run_compress.py``. See
``run_compress_parallel.py`` for a multiprocessing version.
"""

from glob import glob

from readjson import process_compressed

files = glob("../data/*0.5.json")
files = [fn[:-5] for fn in files]

for f in files:
    print(f)
    process_compressed(f)
