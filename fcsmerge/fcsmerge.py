#!/usr/bin/env python
# coding: utf-8

import fcsparser
import numpy as np
import pandas as pd
import os
import fcswrite

from sklearn.neighbors import NearestNeighbors
from constants import MARKER_NAME_MAP, EMPTY_MARKER_NAMES


def readfcs(fcs):
    """Read the given FCS/LMD file using fcsparser

    Any discrepancies in the marker name is handled accoring to the marker map(see constants.py)

    Args:
        fcs: path of the fcs file to be read.

    Returns:
        Compensated FCS data segment as a dataframe
    """

    _, s = fcsparser.parse(fcs)
    s = s.rename(MARKER_NAME_MAP, axis='columns')
    return s


def mergefiles(path, list_files_to_read):
    """resolve absolute path of FCS files and read each file

    Args:
        path: Source path of FCS files to be merged.
        list_files_to_read: List of FCS filenames that will be merged

    Returns:
        list of FCS dataframes, one per each FCS file
    """

    fcs_data = []
    for file in list_files_to_read:
        fcs = os.path.join(path, file)
        fcs_data.append(readfcs(fcs))
    return fcs_data


def nn(list_df, common):
    """Comput nearest neighbor between all tubes.

    Args:
        list_df: List of FCS dataframes to be merged.
        common: List of common/shared markers that is used as the vector to compute NN.

    Returns:
        Merged dataframe: This dataframe contains events from all tubes, with each event now having all the measured markers.
    """

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
            markertube = [item for item in addtube_markers if item not in merged_df.columns]
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

    The new FCS File will be stored in the path: <outpath>/<cohort>/<caseid>_merged.fcs

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
    fname = caseid + "_merged.fcs"
    fcs_filename = os.path.join(outpath, fname)

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    channels, event_count = fcs_write(merged_fcs, fcs_filename)
    newpath = os.path.join(cohort, fname)

    return newpath, channels, event_count


def fcs_write(df, fname):
    """Write the merged FCS data into a new file
    given the FCS data, creates a new file in FCS3.0 format

    Args:
        df: FCS dataframe
        fname: Output file name

    Returns:
        new event count for the merged file and channel names
    """

    data = df.to_numpy()
    channels = list(df.columns)

    # replace any spaces in the marker names to "-" for consistency
    channels = [x.replace(" ", "-") for x in channels]

    fcswrite.write_fcs(filename=fname,
                       chn_names=channels,
                       data=data)
    event_count = data.shape[0]
    return channels, event_count
