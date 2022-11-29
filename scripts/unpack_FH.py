from pathlib import Path
import sys
import pprint

import picklelime.unpack_barspec_fh as ub
from picklelime.util import read_config
from picklelime.util import find_file


if len(sys.argv) == 2:
    config = read_config(sys.argv[1])
else:
    print("no config yaml given")
    exit()

pprint.pprint(config["momdict"])

for filename in config["filenamelist"]:
    # output = filename[:-4] + "/"
    output_dir = Path(config["savelocation"])
    # print(str(output_dir))
    output_dir.mkdir(parents=True, exist_ok=True)
    filename_loc = find_file("config", config["lattice_name"], filename)
    # filename_loc = find_file("config", filename)
    # print(filename_loc)
    with open(filename_loc, "r") as f:
        config_list = [line.strip() for line in f]
    config_list.sort()
    print(len(config_list))
    ub.unpack_barspec_FH(config_list, loc=str(output_dir), momdict=config["momdict"])


# momdict = {
#     "op8_q+0+0+0": [[0, 0, 0]],
#     "": [
#         [0, 0, 0]
#     ],
# }

# ub.unpack_barspec_FH(
#     filelist,
#     loc="/scratch/usr/hhpmbate/limepickle/32x64/b5p50kp120900kp120900/lp0001_cv3_q000/",
#     # momdict=momdict,
# )


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
