import argparse
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--fig-size", nargs="+", type=int, default=(2, 2))
    args = parser.parse_args()

    # figure creation
    fig, ax = plt.subplots(figsize=args.fig_size)

    with open(args.data_path) as f:
        line_list = f.read().splitlines()

        x = [float(n) for n in line_list[1].split(",")]
        y = [float(n) for n in line_list[0].split(",")]

        ax.scatter(x, y)

        for i in range(2, len(line_list), 2):
            x = [float(n) for n in line_list[i + 1].split(",")]
            y = [float(n) for n in line_list[i].split(",")]
            ax.plot(x, y)

    plt.tight_layout()
    plt.savefig("rsme.pdf")


if __name__ == "__main__":
    main()
