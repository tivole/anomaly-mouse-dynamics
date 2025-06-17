import csv
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

def read_mouse_data(log_file):
    data_by_monitor = {}
    with open(log_file, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            event_type = row[2].strip()
            if event_type != "MOVE":
                continue

            try:
                x = float(row[3])
                y = float(row[4])
                monitor_index = int(row[1].strip())
            except ValueError:
                continue

            if monitor_index not in data_by_monitor:
                data_by_monitor[monitor_index] = {"xs": [], "ys": []}
            data_by_monitor[monitor_index]["xs"].append(x)
            data_by_monitor[monitor_index]["ys"].append(y)

    # convert lists to numpy arrays
    for monitor in data_by_monitor:
        data_by_monitor[monitor]["xs"] = np.array(data_by_monitor[monitor]["xs"])
        data_by_monitor[monitor]["ys"] = np.array(data_by_monitor[monitor]["ys"])
    return data_by_monitor

def save_heatmaps(data_by_monitor, output_dir, bins=100):
    if not data_by_monitor:
        print("No MOVE events found in the log file.")
        return

    os.makedirs(output_dir, exist_ok=True)

    for monitor_index, vals in sorted(data_by_monitor.items()):
        xs = vals["xs"]
        ys = vals["ys"]

        fig, ax = plt.subplots(figsize=(10, 6))
        hb = ax.hist2d(xs, ys, bins=bins, cmap='hot')
        ax.invert_yaxis()
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title(f'Mouse Dynamics Heatmap (Monitor {monitor_index})')
        plt.colorbar(hb[3], ax=ax, label='Event Count')
        plt.tight_layout()

        out_path = os.path.join(output_dir, f"heatmap_monitor_{monitor_index}.png")
        fig.savefig(out_path, dpi=120)
        plt.close(fig)
        print(f"Saved heatmap for monitor {monitor_index} to {out_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate and save mouse movement heatmaps from a telemetry log."
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to the mouse telemetry CSV log (e.g. data/mouse_telemetry.log)"
    )
    parser.add_argument(
        "--output_dir", "-o", required=True,
        help="Directory to save generated heatmap images (e.g. images/heatmaps/)"
    )
    parser.add_argument(
        "--bins", "-b", type=int, default=100,
        help="Number of bins per axis for the 2D histogram (default: 100)"
    )
    args = parser.parse_args()

    data_by_monitor = read_mouse_data(args.input)
    save_heatmaps(data_by_monitor, args.output_dir, bins=args.bins)

if __name__ == "__main__":
    main()
