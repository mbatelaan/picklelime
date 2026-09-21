import picklelime.unpack_messpec_fh as umfh
import picklelime.unpack_messpec as um
from pathlib import Path

filenamelist = [
    "meson_qcdsf.lst"
    # "meson_qcdsf.common.lst",
]

outputdir="./test/pickles/"

for filename in filenamelist:
    print("\n\n\n\n", filename)
    output = filename.split(".")[0]+"/"
    with open(filename,'r') as f:
        config_list = [line.strip() for line in f]
    config_list.sort()
    um.unpack_messpec(
        config_list,
        loc=outputdir + output,
    )
