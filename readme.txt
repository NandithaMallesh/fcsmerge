FCSmerge.py:
	merge the fcs data from all tubes and calculate missing value
	approach:
		for each tube:
		  for each event, find nearest neighbour in other tubes, copy missing markers
		  
merge.py:
	./merge.py "FCS datapath" "outputpath" "meta_info.json path" "panel"
	
berlin_merge.py:
	./merge.py "FCS datapath" "outputpath" "meta_info.json path" "panel"
	

Dependencies:
	FlowCal
	fcswrite

Note:
For Bonn _old_set: ignore CD45 for merge 
	- add it to the EMPTY_MARKER_NAMES_LIST in FCSmerge(some samples have CD45 and some don't; mostly normal samples have CD45)