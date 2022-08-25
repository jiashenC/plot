import matplotlib

matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42


COLOR = {
    "red": "#ff5964",
    "blue": "#3f72af",
    "gray": "#ede7e3",
    "yellow": "#ffa62b",
    "green": "#4e9f3d",
    "purple": "#b19cd9",
}

MARKER = {
    "triangle": "^",
    "circle": "o",
    "cross": "X",
    "diamond": "d",
    "plus": "P",
    "star": "*",
}

LINE = {
    "solid": "solid",
    "dotted": "dotted",
    "dashed": (0, (5, 10)),
    "dotteddashed": (0, (3, 5, 1, 5, 1, 5)),
}

BAR_WIDTH = 1
BAR_GAP = 5