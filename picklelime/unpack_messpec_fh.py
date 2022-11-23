# %%
import gc
import copy
import numpy as np
import xml.etree.ElementTree as ET
import os
import itertools
import psutil
import sys
import gc
import pickle as pickle
import collections
from psutil import virtual_memory
import picklelime.core_functions as cf

magic_bytes = b"Eg\x89\xab"
Nd = 4


def readlimefile(
    filename, data, momdict, datasets, filenumber, gamma_combinations=None
):
    with open(filename, "rb") as file_in:
        head, record = cf.ReadRecord(file_in)
        # print("size =", sys.getsizeof(record) / 1024)
        if head[:4] != magic_bytes:
            raise IOError("Record header missing magic bytes.")

        if not head[16:].startswith(b"qcdsfDir"):
            raise IOError("Missing qcdsfDir record")

        tree = ET.ElementTree(ET.fromstring(record.decode("utf-8", "ignore")))
        root = tree.getroot()
        latt_size = [
            int(s)
            for s in root.find("ProgramInfo")
            .find("Setgeom")
            .find("latt_size")
            .text.split(" ")
        ]
        seen = set()
        latt_size_str = "x".join(
            str(x) for x in latt_size if not (x in seen or seen.add(x))
        )
        # time_rev = root.find("Input").find("Param").find("time_rev").text == "true"
        # print("\n\ntime_rev = ", time_rev)
        # Fix time-rev to false for now
        # time_rev = False

        mom2_max = int(root.find("Input").find("Param").find("mom2_max").text)
        num_mom, mom_list = cf.CountMom(mom2_max, Nd)

        head, record = cf.ReadRecord(file_in)
        # print("size =", sys.getsizeof(record) / 1024)

        while head != b"":
            if not head[16:].startswith(b"meta-xml"):
                raise IOError("Expecting meta-xml record")
            tree = ET.ElementTree(ET.fromstring(record.decode("utf-8", "ignore")))
            root = tree.getroot()

            # has_third = not (
            #     root.find("Forward_prop_headers").find("Third_forward_prop") == None
            # )

            # baryon_number = int(root.find("baryon-number").text)

            kappa1 = float(
                root.find("Forward_prop_headers")
                .find("First_forward_prop")
                .find("ForwardProp")
                .find("FermionAction")
                .find("Kappa")
                .text
            )
            kappa2 = float(
                root.find("Forward_prop_headers")
                .find("Second_forward_prop")
                .find("ForwardProp")
                .find("FermionAction")
                .find("Kappa")
                .text
            )

            kappa_str = (
                "k"
                + f"{kappa1:.6f}".lstrip("0").replace(".", "p")
                + "k"
                + f"{kappa2:.6f}".lstrip("0").replace(".", "p")
            )

            ferm_act_string_1 = (
                root.find("Forward_prop_headers")
                .find("First_forward_prop")
                .find("ForwardProp")
                .find("FermionAction")
                .find("FermAct")
                .text.lower()
            )
            ferm_act_string_2 = (
                root.find("Forward_prop_headers")
                .find("Second_forward_prop")
                .find("ForwardProp")
                .find("FermionAction")
                .find("FermAct")
                .text.lower()
            )
            # print(ferm_act_string_1, ferm_act_string_2)

            feynhellopstring = ""
            feynhellstring = ""
            if ferm_act_string_1[-8:] == "feynhell":
                for elem in (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("ForwardProp")
                    .find("FermionAction")
                    .find("FeynHellParam")
                    .findall("elem")
                ):
                    op = elem.find("Operator").text
                    lr = float(elem.find("LambdaReal").text)
                    li = float(elem.find("LambdaImag").text)
                    # mom = elem.find("Momentum").text.replace(" ", "")
                    mom = [
                        int(i) for i in elem.find("Momentum").text.strip(" ").split(" ")
                    ]
                    mom_str = "".join([f"{p_i:+d}" for p_i in mom])

                    # Check whether the lambdas for this operator are non-zero
                    if lr != 0 or li != 0:
                        # Get the exponent of the lambda values
                        charnum = max(len(str(lr)), len(str(li))) - 2
                        # Reformat the lambda values
                        lrs = f"{lr:.{charnum}f}".lstrip("0").replace(".", "p")
                        lis = f"{li:.{charnum}f}".lstrip("0").replace(".", "p")
                        feynhellopstring += f"op{op}_q{mom_str}_"
                        feynhellstring += f"l{lrs}+{lis}i_"
                feynhellstring = feynhellstring.strip("_")
                feynhellopstring = feynhellopstring.strip("_")
            else:
                feynhellstring += "lp0lp0"
                # feynhellopstring += "unpert"

            # To separate the doubly represented from the singly represented quark
            feynhellstring += "__"

            if ferm_act_string_2[-8:] == "feynhell":
                for elem in (
                    root.find("Forward_prop_headers")
                    .find("Second_forward_prop")
                    .find("ForwardProp")
                    .find("FermionAction")
                    .find("FeynHellParam")
                    .findall("elem")
                ):
                    op = elem.find("Operator").text
                    lr = float(elem.find("LambdaReal").text)
                    li = float(elem.find("LambdaImag").text)
                    # mom = elem.find("Momentum").text.replace(" ", "")
                    mom = [
                        int(i) for i in elem.find("Momentum").text.strip(" ").split(" ")
                    ]
                    mom_str = "".join([f"{p_i:+d}" for p_i in mom])

                    # Check whether the lambdas for this operator are non-zero
                    if lr != 0 or li != 0:
                        # Get the exponent of the lambda values
                        charnum = max(len(str(lr)), len(str(li))) - 2
                        # Reformat the lambda values
                        lrs = f"{lr:.{charnum}f}".lstrip("0").replace(".", "p")
                        lis = f"{li:.{charnum}f}".lstrip("0").replace(".", "p")
                        feynhellopstring += f"op{op}_q{mom_str}_"
                        feynhellstring += f"l{lrs}+{lis}i_"
                feynhellstring = feynhellstring.strip("_")
                feynhellopstring = feynhellopstring.strip("_")
            else:
                feynhellstring += "lp0lp0"
                # feynhellopstring += "unpert"

            # If both props have the same fermion action
            if ferm_act_string_1 == ferm_act_string_2:
                ferm_act_string = ferm_act_string_1
                # This causes the writing loop to skip these two folders in the case that there is no feynhell operator
                feynhellopstring = ""
                feynhellstring = ""
            # Set the action string to feynhell if one of the props uses it.
            elif (
                ferm_act_string_1 == "unprec_slrc_feynhell"
                or ferm_act_string_2 == "unprec_slrc_feynhell"
            ):
                ferm_act_string = "unprec_slrc_feynhell"
            else:
                ferm_act_string = ferm_act_string_1 + "_" + ferm_act_string_2

            # if ferm_act_string == "clover":
            #     clover_coeff = (
            #         root.find("Forward_prop_headers")
            #         .find("First_forward_prop")
            #         .find("ForwardProp")
            #         .find("FermionAction")
            #         .find("clovCoeff")
            #         .text.lstrip("0")
            #         .replace(".", "p")
            #     )
            #     ferm_act_string += "_" + clover_coeff

            # Chroma throws an error if both props have different smearing, need
            # only check one each at source and sink

            source_string = (
                root.find("SourceSinkType").find("source_type_1").text.lower()
            )
            sink_string = root.find("SourceSinkType").find("sink_type_1").text.lower()

            if source_string == "shell_source":
                source_kind = (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("PropSource")
                    .find("Source")
                    .find("SmearingParam")
                    .find("wvf_kind")
                    .text.lower()
                )
                source_param = (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("PropSource")
                    .find("Source")
                    .find("SmearingParam")
                    .find("wvf_param")
                    .text.lstrip("0")
                    .replace(".", "p")
                )
                source_intparam = (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("PropSource")
                    .find("Source")
                    .find("SmearingParam")
                    .find("wvfIntPar")
                    .text
                )
                source_string = (
                    f"{source_names(source_string)}"
                    + f"_{smearing_names(source_kind)}"
                    + f"_{source_param}_{source_intparam}"
                )
            else:
                source_string = source_names(source_string)
            if sink_string == "shell_sink":
                sink_kind = (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("PropSink")
                    .find("Sink")
                    .find("SmearingParam")
                    .find("wvf_kind")
                    .text.lower()
                )
                sink_param = (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("PropSink")
                    .find("Sink")
                    .find("SmearingParam")
                    .find("wvf_param")
                    .text.lstrip("0")
                    .replace(".", "p")
                )
                sink_intparam = (
                    root.find("Forward_prop_headers")
                    .find("First_forward_prop")
                    .find("PropSink")
                    .find("Sink")
                    .find("SmearingParam")
                    .find("wvfIntPar")
                    .text
                )
                sink_string = (
                    f"{sink_names(sink_string)}"
                    + f"_{smearing_names(sink_kind)}"
                    + f"_{sink_param}_{sink_intparam}"
                )
            else:
                sink_string = sink_names(sink_string)
            source_sink_string = f"{source_string}-{sink_string}"

            head, record = cf.ReadRecord(file_in)
            # print("size =", sys.getsizeof(record) / 1024)

            # Sanity check
            if not head[16:].startswith(b"mesons-bin"):
                raise IOError("Expecting mesons-bin record")

            record = np.frombuffer(record, ">f8").reshape(
                16, 16, num_mom, latt_size[3], 2
            )

            for n, p in enumerate(mom_list):
                # Check whether momdict exists and whether the current momentum is included in momdict
                if momdict == None or (
                    (feynhellopstring in momdict) and (p in momdict[feynhellopstring])
                ):
                    p_str = "p" + "".join([f"{p_i:+d}" for p_i in p])
                    for gamma1, gamma2 in itertools.product(range(16), range(16)):
                        if (gamma_combinations == None) or (
                            [gamma1, gamma2] in gamma_combinations
                        ):
                            gamma_str = f"{gammaString(gamma1)}-{gammaString(gamma2)}"
                            record_sliced = record[gamma1, gamma2, n]
                            if (
                                type(
                                    data[latt_size_str][ferm_act_string][kappa_str][
                                        feynhellopstring
                                    ][feynhellstring][source_sink_string][p_str][
                                        gamma_str
                                    ]
                                )
                                == collections.defaultdict
                                and len(
                                    data[latt_size_str][ferm_act_string][kappa_str][
                                        feynhellopstring
                                    ][feynhellstring][source_sink_string][p_str][
                                        gamma_str
                                    ].keys()
                                )
                                == 0
                            ):
                                data[latt_size_str][ferm_act_string][kappa_str][
                                    feynhellopstring
                                ][feynhellstring][source_sink_string][p_str][
                                    gamma_str
                                ] = [
                                    record_sliced
                                ]
                                datasets += 1
                                filenumber += 1
                            else:
                                data[latt_size_str][ferm_act_string][kappa_str][
                                    feynhellopstring
                                ][feynhellstring][source_sink_string][p_str][
                                    gamma_str
                                ].append(
                                    record_sliced
                                )
                                datasets += 1
                    else:
                        None

            head, record = cf.ReadRecord(file_in)
            # print("size =", sys.getsizeof(record) / 1024)
        # del record
        # del head
        # gc.collect()
    return data, datasets, filenumber


def unpack_messpec_FH(filelist_iter, loc=".", momdict=None):
    """Unpack messpec files which includ propagators with Feynman-Hellmann perturbations to the action.

    This works very similarly to the unpack_messpec function but it has two added levels which it loops over, the feynhell operator and the feynhell parameters (lambdas). It also takes a dictionary as input which can specify the momentum values to be unpacked for each feynhellopstring.
    """
    data = rec_dd()

    file_count = 0
    emergency_dumps = 0
    max_memory = virtual_memory().total / 4
    file_size = os.path.getsize(filelist_iter[0])
    check_interval = max_memory // file_size

    filenumber = 0
    datasets = 0
    gamma_combinations = [
        [15, 15],
        [15, 7],
        [7, 15],
        [7, 7],
        [1, 1],
        [1, 2],
        [1, 4],
        [1, 8],
        [2, 1],
        [2, 2],
        [2, 4],
        [2, 8],
        [4, 1],
        [4, 2],
        [4, 4],
        [4, 8],
        [8, 1],
        [8, 2],
        [8, 4],
        [8, 8],
    ]

    # Reading in the data by opening each file in turn
    print("reading limes")
    for ifile, filename in enumerate(filelist_iter):
        print(f"file {ifile}/{len(filelist_iter)}")
        # print("datasets = ",datasets)
        # print("filenumber = ",filenumber)
        data, datasets, filenumber = readlimefile(
            filename, data, momdict, datasets, filenumber
        )

    print(f"datasets = {int(datasets)}")
    print(f"filenumber = {int(filenumber)}")
    # print(f"configuration number = {int(datasets/filenumber)}")
    print(43 * "-" + f"\n\twriting {int(filenumber)} pickle files\n" + 43 * "-")

    counter = 0
    for latt_size, lvl1 in data.items():
        for ferm_act, lvl2 in lvl1.items():
            for kappa, lvl3 in lvl2.items():
                for op_val, lvl4 in lvl3.items():
                    for lmb_val, lvl5 in lvl4.items():
                        for source_sink, lvl6 in lvl5.items():
                            for p, lvl7 in lvl6.items():
                                out_dir = (
                                    loc
                                    + f"/messpec/{latt_size}/{ferm_act}/{kappa}/{op_val}/{lmb_val}"
                                    + f"/{source_sink}/{p}/"
                                )

                                os.system(f"mkdir -p {out_dir}")

                                # Save all mesons in one big file
                                ncfg = len(list(lvl7.values())[0])
                                # print("\n\nshape: ", np.shape(list(lvl7.values())))
                                # print("shape: ", np.shape(list(lvl7.values())[0]))
                                # print("shape: ", list(lvl7.values())[0][0])
                                # print("shape: ", list(lvl7.values())[0][1])
                                # print("shape: ", np.shape(list(lvl7.values())[0][0][0]))
                                out_name = f"messpec_full_{ncfg}cfgs.pickle"
                                with open(out_dir + out_name, "wb") as file_out:
                                    pickle.dump(lvl7, file_out)

                                # # Save each meson as an individual file (16x16 files)
                                # for mes, lvl8 in lvl7.items():
                                #     # counter += 1
                                #     ncfg = len(lvl8)
                                #     out_name = f"messpec_{mes}_{ncfg}cfgs.pickle"
                                #     with open(out_dir + out_name, "wb") as file_out:
                                #         pickle.dump(np.array(lvl8), file_out)

    process = psutil.Process()
    print(process.memory_info().rss / 1024**2)  # in bytes
    return


def rec_dd():
    return collections.defaultdict(rec_dd)


def source_names(name):
    names = {"shell_source": "sh", "point_source": "pt"}
    return names[name]


def sink_names(name):
    names = {"shell_sink": "sh", "point_sink": "pt"}
    return names[name]


def smearing_names(name):
    names = {"gauge_inv_jacobi": "gij"}
    return names[name]


def gammaCombinations(n):
    combinations = [
        [15, 15],
        [15, 7],
        [7, 15],
        [7, 7],
        [1, 1],
        [1, 2],
        [1, 4],
        [1, 8],
        [2, 1],
        [2, 2],
        [2, 4],
        [2, 8],
        [4, 1],
        [4, 2],
        [4, 4],
        [4, 8],
        [8, 1],
        [8, 2],
        [8, 4],
        [8, 8],
    ]
    return combinations[n]


def gammaString(n):
    names = [
        "gI",
        "g0",
        "g1",
        "g01",
        "g2",
        "g02",
        "g12",
        "g53",
        "g3",
        "g03",
        "g13",
        "g25",
        "g23",
        "g51",
        "g05",
        "g5",
    ]
    return names[n]


def get_obj_size(obj):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {
            o_id: o
            for o_id, o in all_refr
            if o_id not in marked and not isinstance(o, type)
        }

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz
