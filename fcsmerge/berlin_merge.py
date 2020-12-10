#!/usr/bin/env python
# coding: utf-8


import json
import numpy as np
import fcsmerge
import os
import sys

MARKER_NAME_MAP = {
    "Kappa FITC": "kappa FITC",
    "Lambda PE": "lambda PE",
    "FSC": "FS INT LIN",
    "SSC": "SS INT LIN",
    "*FITC*": "nix",
    "CD5 PacBl": "none",  # some samples in berlin panel have additional CD5 in tube4 instead of none_pb,
    # drop additional CD5; using only tube1 CD5
}

EMPTY_MARKER_NAMES = ["nix", "none", "leer", "TIME", "time"]

# Merge details for each panel
# structure = Panel name: { tubes to merge, common_markers, tube specific markers that are to be merged}
PANEL_MERGE = {
    "Berlin":
        {
            "tubes": ["2", "3", "4"],
            "common_markers":  ["FS INT LIN", "SS INT LIN", "CD19 ECD", "CD45 KrOr"],
            "2": ["FS INT LIN", "SS INT LIN", "Kappa FITC", "Lambda PE", "CD19 ECD", "CD5 PC5.5", "CD38 PC7", "CD10 APC",
                "CD20 PacBl", "CD45 KrOr"],
            "3": ["FS INT LIN", "SS INT LIN", "FMC7 FITC", "CD23 PE", "CD19 ECD", "CD3 PC5", "none PC7", "CD79b APC",
                "CD22 PacBl", "CD45 KrOr"],
            "4": ["FS INT LIN", "SS INT LIN", "CD43 FITC", "IgM PE", "CD19 ECD", "CD25 PC5.5", "CD11c PC7", "CD103 APC",
                "CD45 KrOr"],
        },
}


def print_usage():
    """print syntax of script invocation"""
    print("\nUsage:")
    print("python {0:} datapath outputpath metainfojson(along with path) panel\n".format(os.path.basename(sys.argv[0])))
    return


def map_elements(x):
    return MARKER_NAME_MAP.get(x, x)


def checkmarkers(tubemarker, tubechecker):
    check = True
    marker_list = list(map(map_elements, tubemarker))
    tubechecker = list(map(map_elements, tubechecker))
    for m in marker_list:
        if m not in tubechecker:
            if any(xs in m for xs in EMPTY_MARKER_NAMES):
                continue
            else:
                return False

    return check


def replace_samples(case, new_path, new_marker_list, new_event_count):
    fp = [{"__fcssample__": {"id": case['samples'][0]["__fcssample__"].get("id"),
                             "case_id": case['samples'][0]["__fcssample__"].get("case_id"),
                             'tube': 1,
                             'date': case['samples'][0]["__fcssample__"].get("date"),
                             'path': new_path,
                             'markers': new_marker_list,
                             'panel': case['samples'][0]["__fcssample__"].get("panel"),
                             'count': new_event_count,
                             'material': case['samples'][0]["__fcssample__"].get('material')}}]

    return fp


def write_json(outpath, c_info):
    json_file = os.path.join(outpath, "data.json")
    with open(json_file, 'w') as outfile:
        json.dump(c_info, outfile, indent=4)


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print_usage()
        raise Exception("Invalid arguments")

    datapath = sys.argv[1]
    outputpath = sys.argv[2]
    meta = sys.argv[3]
    panel = sys.argv[4]

    # get tubes,common_marker for each panel form the constant
    panel_info = PANEL_MERGE[panel]
    tubes = panel_info['tubes']
    common_markers = panel_info['common_markers']

    with open(meta, "r") as f:
        case_info = json.load(f)

    for case in case_info:
        case = case['__case__']
        files_to_merge = []
        markers = []
        tube_check = []
        for tube_info in case['samples']:
            tube_info = tube_info["__fcssample__"]
            if tube_info['tube'] in tubes:
                markers = tube_info.get('markers')
                tube_check = panel_info[tube_info['tube']]
                if checkmarkers(markers, tube_check):
                    files_to_merge.append(tube_info.get('path'))
        print(files_to_merge)
        if files_to_merge and len(files_to_merge) == len(tubes):
            new_path, new_markers, new_event_count = fcsmerge.mergefcs(case['id'], datapath, outputpath,
                                                                       case['group'],
                                                                       files_to_merge, common_markers)
            case['samples'] = replace_samples(case, new_path, new_markers, new_event_count)
    write_json(outputpath, case_info)
