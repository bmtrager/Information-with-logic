from readjson import *
from glob import *

files = glob("../data/*0.5.json")
#files = glob("../data/*1.0.json")
files = [fn[:-5] for fn in files]

#[process_compressed(f) for f in files]

for f in files :
    print(f)
    process_compressed(f)


