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
    parser.add_argument(
        "--stack",
        action="store_true",
        default=False,
        help="Whether to draw stacked bar plots.",
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

    sub_cat_length, sub_cat, sub_cat_data = 0, [], []
    cat = []

    # collect data
    with open(args.data_path) as f:
        for i, line in enumerate(f.read().splitlines()):
            if i == 0:
                sub_cat = line.split(",")
                sub_cat_length = len(sub_cat)
                sub_cat_data = [[] for _ in range(sub_cat_length)]
            else:
                for i, d in enumerate(line.split(",")):
                    if i < sub_cat_length:
                        sub_cat_data[i].append(float(d))
                    else:
                        cat.append(d)

    # figure creation
    fig, ax = plt.subplots(figsize=args.fig_size)

    # draw bar chart
    if args.stack:
        bottom = np.zeros(len(cat))
        for i in range(sub_cat_length):
            x = np.arange(len(cat)) * (BAR_WIDTH + BAR_GAP)
            height = sub_cat_data[i]
            ax.bar(x, height, color=color[i], bottom=bottom, label=sub_cat[i])
            bottom += height
        xtick_list = np.arange(len(cat)) * (BAR_WIDTH + BAR_GAP)
        xtick_label_list = cat
    else:
        for i in range(sub_cat_length):
            x = (
                np.arange(len(cat)) * (sub_cat_length * BAR_WIDTH + BAR_GAP)
                + i * BAR_WIDTH
            )
            height = sub_cat_data[i]
            ax.bar(x, height, color=color[i], label=sub_cat[i])
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
    plt.savefig("bar.pdf")


if __name__ == "__main__":
    main()
