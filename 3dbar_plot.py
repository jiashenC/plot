#!/usr/bin/env python3
import argparse
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

from config import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        required=True,
        type=str,
        help="Data file path.",
    )
    parser.add_argument("--fig-size", nargs="+", type=int, default=(5, 2))
    args = parser.parse_args()

    color = [
        COLOR["red"],
        COLOR["blue"],
        COLOR["purple"],
        COLOR["yellow"],
        COLOR["green"],
    ]

    hatch = [
        HATCH["left"],
        HATCH["right"],
        HATCH["dot"],
    ]

    sub_cat_repeat, sub_cat_length, sub_cat, sub_cat_data_group = 0, 0, [], []
    cat = set([])

    repeat_idx = 0

    # collect data
    with open(args.data_path) as f:
        for i, line in enumerate(f.read().splitlines()):
            if i == 0:
                sub_cat = line.split(",")
                sub_cat_length = len(sub_cat) - 1
                sub_cat_repeat = int(sub_cat[-1])
                sub_cat_data_group = [
                    [[] for _ in range(sub_cat_length)] for _ in range(sub_cat_repeat)
                ]
            else:
                for k, d in enumerate(line.split(",")):
                    if k < sub_cat_length:
                        sub_cat_data_group[repeat_idx][k].append(float(d))
                    else:
                        cat.add(d)
                repeat_idx = (repeat_idx + 1) % sub_cat_repeat

    # figure creation
    fig, ax = plt.subplots(figsize=args.fig_size)

    for i in range(sub_cat_length):
        bottom = np.zeros(len(cat))
        for k in range(sub_cat_repeat):
            x = (
                np.arange(len(cat)) * (sub_cat_length * BAR_WIDTH + BAR_GAP)
                + i * BAR_WIDTH
            )
            height = sub_cat_data_group[k][i]
            if k == 0:
                ax.bar(x, height, color=color[i], bottom=bottom, label=sub_cat[i])
            else:
                ax.bar(x, height, color=color[i], bottom=bottom, hatch=hatch[k - 1])
            bottom += np.array(height)
    xtick_list = (
        np.arange(len(cat)) * (sub_cat_length * BAR_WIDTH + BAR_GAP)
        + sub_cat_length * BAR_WIDTH / 2
        - BAR_WIDTH / 2
    )
    xtick_label_list = cat

    ax.set_xticks(xtick_list)
    ax.set_xticklabels(xtick_label_list)

    plt.legend(
        ncol=sub_cat_length,
        frameon=False,
        fancybox=False,
        bbox_to_anchor=(0.5, 1.1),
        loc="center",
    )

    plt.tight_layout()
    plt.savefig("3dbar.png")


if __name__ == "__main__":
    main()
