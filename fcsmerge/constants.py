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
}

# Empty channels to drop
EMPTY_MARKER_NAMES = ["nix", "none", "leer", "TIME"]


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
}
