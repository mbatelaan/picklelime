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

#==================================================    
# For FH runs    
# momdict = {
#     "op2_q+6+4+2_op2_q-6-4-2": [[-3, -2, -1], [3, 2, 1]],
#     "op8_q+6+4+2_op8_q-6-4-2": [[-3, -2, -1], [3, 2, 1]],
#     "op2_q+6+0+0_op2_q-6+0+0": [[-3, 0, 0], [3, 0, 0]],
#     "op8_q+6+0+0_op8_q-6+0+0": [[-3, 0, 0], [3, 0, 0]],
#     "op2_q+4+4+2_op2_q-4-4-2": [[-2, -2, -1], [2, 2, 1]],
#     "op8_q+4+4+2_op8_q-4-4-2": [[-2, -2, -1], [2, 2, 1]],
#     "op2_q+4+2+2_op2_q-4-2-2": [[-2, -1, -1], [2, 1, 1]],
#     "op8_q+4+2+2_op8_q-4-2-2": [[-2, -1, -1], [2, 1, 1]],
#     "op2_q+2+2+0_op2_q-2-2+0": [[-1, -1, 0], [1, 1, 0]],
#     "op8_q+2+2+0_op8_q-2-2+0": [[-1, -1, 0], [1, 1, 0]],
#     "op8_q+0+0+0_op8_q+0+0+0": [[0, 0, 0]],
#     "": [
#         [-3, -2, -1],
#         [-3, 0, 0],
#         [-2, -2, -1],
#         [-2, -1, -1],
#         [-1, -1, 0],
#         [0, 0, 0],
#         [1, 1, 0],
#         [2, 1, 1],
#         [2, 2, 1],
#         [3, 0, 0],
#         [3, 2, 1],
#     ],
# }

# mom = [-6, -4, -2]
# fhstring = "op2_q642_op2_q-6-4-2"
# print(fhstring in momdict)
# print(mom in momdict[fhstring])

# ub.unpack_barspec_FH(
#     filelist_smsnk30,
#     loc="/scratch/usr/hhpmbate/limepickle/output/",
#     momdict=momdict,
# )
    
