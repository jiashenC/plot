#!/usr/bin/env python3

import math
import argparse
import numpy as np
import matplotlib.pyplot as plt

from fractions import Fraction

from config import *


def log2(x):
    return math.log(x, 2)


def find_start_point(min_x_tick, min_y_tick, slope):
    if min_x_tick * slope < min_y_tick:
        return log2(min_y_tick / slope), log2(min_y_tick)
    else:
        return log2(min_x_tick), log2(min_x_tick * slope)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--roofline-data-path",
        type=str,
        nargs="+",
        required=True,
        help="Roofline file path.",
    )
    parser.add_argument(
        "--algorithm-data-path",
        type=str,
        nargs="+",
        required=True,
        help="Algorithm file path.",
    )
    parser.add_argument("--fig-size", nargs="+", type=int, default=(5, 4))
    args = parser.parse_args()

    linestyle_list = [LINE["solid"], LINE["dotted"]]
    color_list = [
        COLOR["green"],
        COLOR["yellow"],
        COLOR["gray"],
        COLOR["purple"],
    ]
    marker_list = [
        MARKER["triangle"],
        MARKER["circle"],
        MARKER["cross"],
        MARKER["diamond"],
    ]

    # collect algorithm data points first
    # needed for plotting the x and y axis for
    # the roofline model
    min_x, max_x, min_y, max_y = 0xFFFFFFFF, 0, 0xFFFFFFFF, 0

    all_x_list, all_y_list, all_label_list = [], [], []
    for path in args.algorithm_data_path:
        with open(path, "r") as f:
            x_list, y_list = [], []
            for i, line in enumerate(f.read().splitlines()):
                if i == 0:
                    all_label_list.append(line)
                else:
                    x, y = line.split(",")

                    x = log2(float(x))
                    y = log2(float(y))

                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)

                    x_list.append(x)
                    y_list.append(y)

            all_x_list.append(x_list)
            all_y_list.append(y_list)

    # collect min and max ticks
    x_tick_list, y_tick_list = [], []
    x_tick_label_list, y_tick_label_list = [], []

    power = -100
    value = 2**power

    while True:
        if power > 100:
            break

        if (
            min_x < power < max_x
            or (power + 1 > min_x and power < max_x)
            or (power - 4 < max_x and power > min_x)
        ):
            x_tick_list.append(power)
            if power < 0:
                x_tick_label_list.append(
                    Fraction(1 / 2**-power).limit_denominator()
                )
            else:
                x_tick_label_list.append(int(value))

        if (
            min_y < power < max_y
            or (power + 1 > min_y and power < max_y)
            or (power - 1 < max_y and power > min_y)
        ):
            y_tick_list.append(power)
            if power < 0:
                y_tick_label_list.append(
                    Fraction(1 / 2**-power).limit_denominator()
                )
            else:
                y_tick_label_list.append(int(value))

        power += 1
        value *= 2

    min_x_tick, max_x_tick = min(x_tick_list), max(x_tick_list)
    min_y_tick, max_y_tick = min(y_tick_list), max(y_tick_list)

    # figure creation
    fig, ax = plt.subplots(figsize=args.fig_size)

    # draw the ceilings first
    x_vals_list = []
    for i, path in enumerate(args.roofline_data_path):
        with open(path, "r") as f:
            out = f.read().splitlines()

            line = out[0]
            label_slant, label_hori = line.split(",")

            line = out[1]
            mem_bandwidth = float(line.split(",")[0])
            compute_bandwidth = float(line.split(",")[1])

            mem_x1, mem_y1 = min_x_tick, log2(mem_bandwidth * 2**min_x_tick)
            mem_x2, mem_y2 = (
                log2(compute_bandwidth / mem_bandwidth),
                log2(compute_bandwidth),
            )

            compute_x1, compute_y1 = mem_x2, log2(compute_bandwidth)
            compute_x2, compute_y2 = max_x_tick, log2(compute_bandwidth)

            ax.plot(
                [mem_x1, mem_x2],
                [mem_y1, mem_y2],
                linestyle=linestyle_list[i],
                color=COLOR["red"],
            )
            slope = np.rad2deg(
                np.arctan2(
                    mem_y2 - mem_y1,
                    mem_x2 - mem_x1,
                )
            )
            start_point = find_start_point(
                2**min_x_tick,
                2**min_y_tick,
                (2**mem_y2 - 2**mem_y1) / (2**mem_x2 - 2**mem_x1),
            )
            text = ax.text(
                log2(2 ** ((mem_x2 + start_point[0]) / 2)),
                log2(2 ** ((mem_y2 + start_point[1]) / 2)) + 0.2,
                label_slant,
                horizontalalignment="center",
                verticalalignment="center",
                rotation_mode="anchor",
                color=COLOR["red"],
                transform_rotates_text=True,
            )
            text.set_rotation(slope)

            ax.plot(
                [compute_x1, compute_x2],
                [compute_y1, compute_y2],
                linestyle=linestyle_list[i],
                color=COLOR["blue"],
            )
            ax.text(
                log2(2 ** ((compute_x1 + compute_x2) / 2)),
                log2(2 ** ((compute_y1 + compute_y2) / 2)) + 0.2,
                label_hori,
                horizontalalignment="center",
                verticalalignment="center",
                color=COLOR["blue"],
            )

    idx = 0
    for x_list, y_list in zip(all_x_list, all_y_list):
        ax.scatter(
            x_list,
            y_list,
            color=color_list[idx],
            marker=marker_list[idx],
            label=all_label_list[idx],
            zorder=0xFFFFFFFF,
        )
        idx += 1

    ax.set_xticks(x_tick_list)
    ax.set_xticklabels(x_tick_label_list)
    ax.set_yticks(y_tick_list)
    ax.set_yticklabels(y_tick_label_list)

    ax.set_xlim(min(x_tick_list), max(x_tick_list))
    ax.set_ylim(min(y_tick_list), max(y_tick_list))

    ax.set_xlabel("Arithmetic Intensity (ops/byte)", {"fontweight": "bold"})
    ax.set_ylabel("Attainable Bandwidth (Gops/sec)", {"fontweight": "bold"})

    plt.tight_layout()
    plt.savefig("roofline.pdf")


if __name__ == "__main__":
    main()
