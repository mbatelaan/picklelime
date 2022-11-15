import unpack_barspec_fh as ub
from pathlib import Path

with open('filelist.lst','r') as f:
  filelist = [line.strip() for line in f]

momdict = {
    "op8_q+0+0+0": [[0, 0, 0]],
    "": [
        [0, 0, 0]
    ],
}

ub.unpack_barspec_FH(
    filelist,
    loc="/scratch/usr/hhpmbate/limepickle/32x64/b5p50kp120900kp120900/lp0001_cv3_q000/",
    # momdict=momdict,
)


# filenamelist = [ "baryon_qcdsf.lst" ]
# for filename in filenamelist:
#     output = filename[:-4]+"/"
#     with open(filename,'r') as f:
#         config_list = [line.strip() for line in f]
#     config_list.sort()
#     ub.unpack_barspec_FH(
#         config_list,
#         loc="./"+output,
#         momdict=momdict
#     )
