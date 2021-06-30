# FCS Merge: merge fcs data from all tubes for each sample and impute missing values for the non-shared markers

## Approach: 
* Step 1: For each tube(i), find nearest neighbour of every event in the other tubes(j) using the shared markers.
* Step 2: For each event in tube i, copy missing markers from tubes j. 
* Step 3: Repeat the process between all tubes such that events in one tube have imputed values for all non-shared markers that were originally measured in  different tubes.

### Requirements
Install the following packages with pip:
* scikit-learn
* fcsparser
* fcswrite

### Data
Download the data sets to be merged from Harvard Dataverse: https://doi.org/10.7910/DVN/CQHHEH

### Scripts
1. **FCSmerge.py:** merge the fcs data from all tubes. compute nearest neighbour and copy missing markers. Create a sinlge larege FCS file
2. **merge.py:** read the meta info and check necessary information for merge
3. **constants.py:** panel information and parameters for merge

### Excution
Once the original FCS data sets are downladed, run the following commands to merge each data set:
* For all panels other than Berlin, use:
	* ./merge.py "FCS datapath" "outputpath" "meta_info.json path" "panel"
	
* For the Berlin panel, the meta info is saved in a different format, run the following command to merge Berlin data set:	
	* ./berlin_merge.py "FCS datapath" "outputpath" "meta_info.json path" "Berlin"

### Parameters
* FCS datapath : path where the original FCS datasets are stored
* outputpath: Output folder path to write the merged FCS files
* meta_info.json path: path to case_info.json
* panel: one of the following
	* Bonn, Bonn_new, MLL9F, MLL5F, Erlangen

### Examples
```
./merge.py "$FCS" "$OUTPUT" "$META" "$PANEL"
	$FCS: path where the original unmerged FCS files are stored
	$OUTPUT: path to save the merged fcs files
	$META: meta_info.json describing the dataset
	$PANEL: panel to retrieve the appropriate merge parameters for each data set

./merge.py "/data/FCS/MLL5F" "Merged_FCS/MLL5F" "/data/FCS/MLL5F/case_info.json" "MLL5F"

```
