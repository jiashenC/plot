#!/usr/bin/env python3


import argparse
import numpy as np
import matplotlib.pyplot as plt

from config import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        required=True,
        type=str,
        help="Data file path.",
    )
    parser.add_argument("--fig-size", nargs="+", type=int, default=(2, 2))
    args = parser.parse_args()

    color = [
        COLOR["red"],
        COLOR["blue"],
        COLOR["purple"],
        COLOR["yellow"],
        COLOR["green"],
    ]

    marker = [
        MARKER["triangle"],
        MARKER["circle"],
        MARKER["cross"],
        MARKER["plus"],
        MARKER["diamond"],
    ]

    # figure creation
    fig, ax = plt.subplots(figsize=args.fig_size)

    with open(args.data_path) as f:
        x_list, y_list, label = None, None, None
        for i, line in enumerate(f.read().splitlines()):
            if i % 2 == 0:
                line_arr = line.split(",")
                y_list = [float(n) for n in line_arr[:-1]]
                label = line_arr[-1]
            else:
                line_arr = line.split(",")
                x_list = [float(n) for n in line_arr]

            if i % 2 == 1:
                ax.plot(x_list, y_list, color=color[i // 2], marker=marker[i // 2], label=label)

    plt.tight_layout()
    plt.savefig("line.pdf")


if __name__ == "__main__":
    main()
