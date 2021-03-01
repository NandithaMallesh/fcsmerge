# FCS Merge: merge fcs data from all tubes and calculate missing value
## Approach: For each tube, find nearest neighbour of every event in the other tubes, copy missing markers. Repeat the process between all tubes such that events in one tube have imputed values for markers that were originally measured in different tubes.

### Scripts
1. **FCSmerge.py:** merge the fcs data from all tubes. compute nearest neighbour and copy missing markers. Create a sinlge larege FCS file
2. **merge.py:** read the meta info and check necessary information for merge
3. **constants.py:** panel information and parameters for merge

### Excution
* ./merge.py "FCS datapath" "outputpath" "meta_info.json path" "panel"
	
* berlin_merge.py:
   * ./berlin_merge.py "FCS datapath" "outputpath" "meta_info.json path" "Berlin"

### Parameters
* FCS datapath : path to original FCS files
* outputpath: Out put folder path to write the merged FCS files
* meta_info.json path: path to case_info.json
* panel: one of the following
	* Bonn, Bonn_new, MLL9F, MLL5F, Erlangen

### Dependencies:
* fcsparser
* fcswrite

### Note:
* For Bonn _old_set: ignore CD45 for merge 
	* add it to the EMPTY_MARKER_NAMES_LIST in FCSmerge(some samples have CD45 and some don't; mostly normal samples have CD45)
