#!/usr/bin/env python
# coding: utf-8

import FlowCal
import numpy as np
import pandas as pd
import os
import fcswrite

from sklearn.neighbors import NearestNeighbors

MARKER_NAME_MAP = {
    "Kappa-FITC": "kappa-FITC",
    "Lambda-PE": "lambda-PE",
    "FSC": "FS INT LIN",
    "SSC": "SS INT LIN",
    "*FITC*": "nix",
    "CD5 PacBl": "none",  # some samples in berlin panel have additional CD5 in tube4 instead of none pb
                          # dropping additional CD5; using only tube1 CD5
}

EMPTY_MARKER_NAMES = ["nix", "none", "leer", "TIME"]


def readfcs(fcs):
    s = FlowCal.io.FCSData(fcs)
    marker_names = []
    # adjust marker name discrepancies
    for i in range(len(s.channels)):
        key = '$P' + str(i + 1) + 'S'
        value = s.text.get(key)
        marker_name = MARKER_NAME_MAP.get(value, value)
        marker_names.append(marker_name)
    return pd.DataFrame(s, columns=marker_names)


def mergefiles(path, list_files_to_read):
    fcs_data = []
    for file in list_files_to_read:
        fcs = os.path.join(path, file)
        fcs_data.append(readfcs(fcs))
    return fcs_data


def nn(list_df, common):
    merged_df = pd.DataFrame()
    concat_merge = []

    for i in range(len(list_df)):
        tube1 = list_df[i]
        rest = [x for j, x in enumerate(list_df) if j != i]
        merged_df = pd.DataFrame(tube1)
        
        for othernum, addtube in enumerate(rest):
            all_values = np.array(addtube[common])
            value = np.array(tube1[common])
            idx = computenn(value, all_values).flatten().tolist()
            addtube_markers = addtube.columns
            markertube = [item for item in addtube_markers if item not in common]
            x = addtube.iloc[idx][markertube].reset_index(drop=True)
            merged_df = pd.concat([merged_df, x], axis=1).reset_index(drop=True)

            drop_column_names = [s for s in merged_df.columns if any(xs in s for xs in EMPTY_MARKER_NAMES)]
            merged_df = merged_df.drop(columns=drop_column_names)

        concat_merge.append(merged_df)
        
    return (pd.concat(concat_merge, sort=False).reset_index(drop=True))


def computenn(values, all_values, nbr_neighbors=1):
    nn = NearestNeighbors(nbr_neighbors, metric='euclidean', algorithm='kd_tree').fit(all_values)
    dists, idxs = nn.kneighbors(values)
    return idxs


def mergefcs(caseid, datapath, outpath, cohort, list_of_files, common_markers):
    """Merge a number of FCS files into a single FCS file.

    The new FCS File will be stored in the path: <outpath>/<cohort>/<caseid>_merged.LMD

    Args:
        caseid: Patient ID. This is used for the automatically generated filename.
        datapath: Source path for FCS file.
        outpath: Output path for merged FCS file.
        cohort: Group subdirectory for output merged FCS file.
        list_of_files: List of FCS filenames that will be merged.
        common_markers: List of marker names that will be merged in the single files.

    Returns:
        Tuple of new merged path, channels in merged path, number of total events.
    """
    list_df = mergefiles(datapath, list_of_files)
    merged_fcs = nn(list_df, common_markers)
    outpath = os.path.join(outpath, cohort)
    fname = caseid + "_merged.LMD"
    fcs_filename = os.path.join(outpath, fname)

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    channels, event_count = fcs_write(merged_fcs, fcs_filename)
    newpath = os.path.join(cohort, fname)

    return newpath, channels, event_count


def fcs_write(df, fname):
    data = df.to_numpy()
    channels = list(df.columns)
    channels = [x.replace(" ", "-") for x in channels]
    print(channels)
    fcswrite.write_fcs(filename=fname,
                       chn_names=channels,
                       data=data)
    event_count = data.shape[0]
    return channels, event_count
