from pathlib import Path
import sys

import picklelime.unpack_bar3ptfn as ub
from picklelime.util import read_config


if len(sys.argv) == 2:
    config = read_config(sys.argv[1])
else:
    print("no config yaml given")

output_dir = Path(config["savelocation"] + output)
output_dir.mkdir(parents=True, exist_ok=True)

for filename in config["filenamelist"]:
    output = filename[:-4] + "/"
    filename_loc = find_file("config", filenamename)
    print(filename_loc)
    exit()
    with open(filename, "r") as f:
        config_list = [line.strip() for line in f]
    config_list.sort()
    ub.unpack_bar3ptfn(config_list, loc=output_dir, momdict=config["momdict"])


# filelist = [ [[str(limedir)+'/' + config + ending + sink + '.lime' for config in config_list] for ending in file_endings] for sink in file_sinks]
# print(filelist[0][0])

# filelist_pntsnk = [val for sublist in filelist[0] for val in sublist]
# print(filelist_pntsnk)

# filelist_smsnk30 = [val for sublist in filelist[1] for val in sublist]
# print(filelist_smsnk30)

# limelist = list(limedir.glob("baryon*.lime"))
# limelist = list(
#     limedir.glob("baryon_qcdsf.840.b5p65kp122130kp121756-48x96.00627_0.000_220*.lime")
# )

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
