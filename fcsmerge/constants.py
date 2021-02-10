"""
Constants and default mappings used for merge
"""

# Marker name normalization to correct for name discrepancies
MARKER_NAME_MAP = {
    "Kappa-FITC": "kappa-FITC",
    "Lambda-PE": "lambda-PE",
    "FSC": "FS INT LIN",
    "SSC": "SS INT LIN",
    "*FITC*": "nix",
    "CD5 PacBl": "none",  # some samples in berlin panel have additional CD5 in tube4 instead of none pb
                          # dropping additional CD5; using only tube1 CD5
    "45-CO": "45-KO",     # additional marker name mapping for Erlangen
    "FL10 INT LOG": "45-KO",
    "43-APC-AF750": "43-APC750",
    "-ECD": "none",
    "FL3 INT LOG": "none",
    "23_PB": "23-PB",
    "5-APC-AF750": "5-APC750",
    "FL7 INT LOG": "none",
    "APC-AF700": "none",
    "Kappa FITC": "kappa FITC",
    "Lambda PE": "lambda PE",

}

# Empty channels to drop
EMPTY_MARKER_NAMES = ["nix", "none", "leer", "TIME", "FS PEAK LIN", "time"]

# Merge details for each panel
# structure = Panel name: { tubes to merge, common_markers, tube specific markers that are to be merged}
PANEL_MERGE = {
    "Bonn":
        {
            "tubes": [1, 2],
            "common_markers": ["FS INT LIN", "SS INT LIN", "CD19-ECD", "CD20-PB"],
            1: ['FS INT LIN', 'SS INT LIN', 'FMC7-FITC', 'CD23-PE', 'CD19-ECD', 'CD11c-PC5.5', 'CD200-PC7', 'CD79b-APC',
                'CD5-AA700', 'CD43-AA750', 'CD20-PB'],
            2: ['FS INT LIN', 'SS INT LIN', 'kappa-FITC', 'lambda-PE', 'CD19-ECD', 'CD10-PC5.5', 'CD22-PC7',
                'CD103-APC', 'CD25-AA700', 'CD38-AA750', 'CD20-PB'],
        },
    "Bonn_new":
        {
            "tubes": [1, 2],
            "common_markers": ["FS INT LIN", "SS INT LIN", "CD19-ECD", "CD20-PB", "CD45-KrOr"],
            1: ['FS INT LIN', 'SS INT LIN', 'FMC7-FITC', 'CD23-PE', 'CD19-ECD', 'CD11c-PC5.5', 'CD200-PC7', 'CD79b-APC',
                'CD5-AA700', 'CD43-AA750', 'CD20-PB', "CD45-KrOr"],
            2: ['FS INT LIN', 'SS INT LIN', 'kappa-FITC', 'lambda-PE', 'CD19-ECD', 'CD10-PC5.5', 'CD22-PC7',
                'CD103-APC', 'CD25-AA700', 'CD38-AA750', 'CD20-PB', "CD45-KrOr"],
        },
    "MLL9F":
        {
            "tubes": [1, 2],
            "common_markers": ["FS INT LIN", "SS INT LIN", "CD19-APCA750", "CD45-KrOr"],
            1: ["FS INT LIN", "SS INT LIN", "FMC7-FITC", "CD10-PE", "IgM-ECD", "CD79b-PC5.5", "CD20-PC7", "CD23-APC",
                "CD19-APCA750", "CD5-PacBlue", "CD45-KrOr"],
            2: ["FS INT LIN", "SS INT LIN", "Kappa-FITC", "Lambda-PE", "CD38-ECD", "CD25-PC5.5", "CD11c-PC7",
                "CD103-APC", "CD19-APCA750", "CD22-PacBlue", "CD45-KrOr"],
        },
    "MLL5F":
        {
            "tubes": [2, 3, 4, 5, 7],
            "common_markers": ["FS INT LIN", "SS INT LIN", "CD19-ECD", "CD45-PC7"],
            2: ["FS INT LIN", "SS INT LIN", "CD79b-FITC", "CD5-PE", "CD19-ECD", "CD20-PC5", "CD45-PC7"],
            3: ["FS INT LIN", "SS INT LIN", "FMC7-FITC", "IgM-PE", "CD19-ECD", "CD10-PC5", "CD45-PC7"],
            4: ["FS INT LIN", "SS INT LIN", "CD103-FITC", "CD23-PE", "CD19-ECD", "CD22-PC5", "CD45-PC7"],
            5: ["FS INT LIN", "SS INT LIN", "Kappa-FITC", "Lambda-PE", "CD19-ECD", "CD38-PC5", "CD45-PC7"],
            7: ["FS INT LIN", "SS INT LIN", "CD11c-PE", "CD19-ECD", "CD25-PC5", "CD45-PC7"],
        },
    "Erlangen":
        {
            "tubes": ["B1", "B2"],
            "common_markers": ["FS INT LIN", "SS INT LIN", "19-PC7", "45-KO"],
            "B1": ["FS INT LIN", "SS INT LIN", "Kappa-FITC", "Lambda-PE", "3-ECD", "20-PC5.5", "19-PC7", "10-APC",
                   "5-APC750", "23-PB", "45-KO"],
            "B2": ["FS INT LIN", "SS INT LIN", "38-FITC", "79b-PE", "11c-PC5.5", "19-PC7", "103-APC", "43-APC-AF750",
                   "HLADR-PB", "45-KO"],
        },

}
