# FCS Merge: merge fcs data from all tubes and calculate missing value
## Approach: For each tube, find find nearest neighbour of every event in the other tubes, copy missing markers. Repeat for all tubes

### Scripts
1. **FCSmerge.py:** merge the fcs data from all tubes. compute nearest neighbour and copy missing markers. Create a sinlge larege FCS file
2. **merge.py:** read the meta info and check necessary infirmation for merge:

### Excution
* ./merge.py "FCS datapath" "outputpath" "meta_info.json path" "panel"
	
* berlin_merge.py:
   * ./berlin_merge.py "FCS datapath" "outputpath" "meta_info.json path" "Berlin"

### Parameters
* FCS datapath : path to original FCS files
* outputpath: Out put folder path to write the merged FCS files
* meta_info.json path: path to case_info.json
* panel: one of the following
	* Bonn, Bonn_new, MLL9F, MLL5F

### Dependencies:
* FlowCal
* fcswrite

### Note:
* For Bonn _old_set: ignore CD45 for merge 
	* add it to the EMPTY_MARKER_NAMES_LIST in FCSmerge(some samples have CD45 and some don't; mostly normal samples have CD45)
