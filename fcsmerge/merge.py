#!/usr/bin/env python
# coding: utf-8

# DO NOT USE THIS FOR BERLIN PANEL, META FILE STRUCTURE IS DIFFERENT

import json
import fcsmerge
import os
import sys

from constants import MARKER_NAME_MAP, EMPTY_MARKER_NAMES, PANEL_MERGE


def print_usage():
    """print syntax of script invocation"""
    print("\nUsage:")
    print("python {0:} datapath outputpath metainfojson(along with path) panel(Bonn, Bonn_new, MLL9F, "
          "MLL5F, Erlangen or Berlin)\n".format(
        os.path.basename(sys.argv[0])))
    return


def map_elements(x):
    return MARKER_NAME_MAP.get(x, x)


def checkmarkers(tubemarker, tubechecker):
    """Check for required markers in each tube 

    The tube-specific markers that are to be merged are desceribed in constants.py

    Args:
        tubemarker: required markers for that tube
        tubechecker: markers in the given tube that needs to be validated

    Returns:
        True if all the required markers are found, False otherwise
    """

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


def replace_filepaths(case, new_path, new_marker_list, new_event_count):
    """Rewrite filepath element of the meta data json for each of the merged sample

    Args:
        case: case id of the sample
        new_path: new file path of the merged FCS file
        new_marker_list: list of marker names in the merged FCS
        new_event_count: new event count of the merged sample

    Returns:
        The modified "filepath" for the give case id
    """

    fp = [{'id': case['id'],
           'panel': case['filepaths'][0].get('panel'),
           'tube': 1,
           'date': case['date'],
           'material': case['filepaths'][0].get('material'),
           'fcs': {'path': new_path,
                   'markers': new_marker_list,
                   'event_count': new_event_count}}]
    return fp


def write_json(out_path, c_info):
    json_file = os.path.join(out_path, "data.json")
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
        files_to_merge = []
        markers = []
        tube_check = []
        for tube_info in case['filepaths']:
            if tube_info['tube'] in tubes:
                markers = tube_info['fcs'].get('markers')
                tube_check = panel_info[tube_info['tube']]
                if checkmarkers(markers, tube_check):
                    files_to_merge.append(tube_info['fcs'].get('path'))

        if files_to_merge and len(files_to_merge) == len(tubes):
            new_path, new_markers, new_event_count = fcsmerge.mergefcs(case['id'], datapath, outputpath,
                                                                       case['cohort'],
                                                                       files_to_merge, common_markers)
            case['filepaths'] = replace_filepaths(case, new_path, new_markers, new_event_count)
    write_json(outputpath, case_info)
