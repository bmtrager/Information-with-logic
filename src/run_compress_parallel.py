"""Regenerate every ``*_compressed_count.json`` summary in parallel.

Run from the ``src`` directory: ``python run_compress_parallel.py``. One worker
process is spawned per test set.
"""

from multiprocessing import Pool
from glob import glob

from readjson import process_compressed

files = glob("../data/*0.5.json")
files = [fn[:-5] for fn in files]

if __name__ == '__main__':
    with Pool(len(files)) as p:
        p.map(process_compressed, files)
