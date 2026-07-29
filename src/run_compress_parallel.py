# invoke this file using : python run_compress_parallel.py

from multiprocessing import Pool
from readjson import *
from glob import *

files = glob("../data/*0.5.json")
#files = glob("../data/*1.0.json")
files = [fn[:-5] for fn in files]

#[process_compressed(f) for f in files]

if __name__ == '__main__':
    with Pool(len(files)) as p:
        p.map(process_compressed, files)


