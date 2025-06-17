import csv
import argparse
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt
import os

def read_mouse_data(log_file):
    monitors = {}
    with open(log_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue

            monitor_index = row[1].strip()
            ev = row[2].strip()

            if monitor_index not in monitors:
                monitors[monitor_index] = {"moves": [], "clicks": [], "scrolls": []}

            try:
                x, y = float(row[3]), float(row[4])
            except ValueError:
                continue

            if ev == "MOVE":
                monitors[monitor_index]["moves"].append((x, y))
            elif ev in ("CLICK_DOWN", "CLICK_UP"):
                monitors[monitor_index]["clicks"].append((x, y))
            elif ev == "SCROLL" and len(row) >= 7:
                dx, dy = float(row[5]), float(row[6])
                monitors[monitor_index]["scrolls"].append((x, y, dx, dy))

    return monitors

def plot_all_events(moves, clicks, scrolls, monitor_index, out_path=None):
    fig, ax = plt.subplots(figsize=(10,6), dpi=120)

    if len(moves):
        mov_line, = ax.plot(
            moves[:,0], moves[:,1],
            linewidth=2, alpha=0.3, color='blue',
            label='Movement'
        )

    if len(clicks):
        click_sc = ax.scatter(
            clicks[:,0], clicks[:,1],
            marker='o', s=30,
            facecolors='none', edgecolors='red',
            label='Clicks'
        )

    arrow_scale = 20
    for x, y, dx, dy in scrolls:
        ax.annotate(
            '', 
            xy=(x + dx * arrow_scale, y + dy * arrow_scale),
            xytext=(x, y),
            arrowprops=dict(
                arrowstyle='->',
                color='green',
                lw=1.8,
                shrinkA=0, shrinkB=0
            )
        )

    ax.invert_yaxis()
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title(f'Mouse dynamics (Monitor {monitor_index})')
    ax.margins(0.02)

    scroll_proxy = Line2D(
        [0], [0],
        linestyle='None',
        marker=r'$\rightarrow$',
        markersize=10,
        color='green',
        label='Scrolls'
    )

    handles, labels = ax.get_legend_handles_labels()
    handles.append(scroll_proxy)
    ax.legend(handles=handles, loc='upper right')

    plt.tight_layout()
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path, dpi=120)
        print(f"Saved plot to {out_path}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot mouse movements, clicks and scrolls from a telemetry log.")
    parser.add_argument("--input", "-i", required=True, help="Path to mouse_telemetry.log CSV file")
    parser.add_argument("--output", "-o", help="Output image path (e.g. visuals/trajectory.png). If omitted, shows interactively.")
    parser.add_argument("--monitor", "-m", default="1", help="Monitor index to plot (default: 1)")
    args = parser.parse_args()

    monitors = read_mouse_data(args.log)
    if args.monitor not in monitors:
        print(f"No data for monitor '{args.monitor}' in {args.log}")
        return

    data = monitors[args.monitor]
    moves = np.array(data["moves"]) if data["moves"] else np.empty((0,2))
    clicks = np.array(data["clicks"]) if data["clicks"] else np.empty((0,2))
    scrolls = data["scrolls"]

    plot_all_events(moves, clicks, scrolls, args.monitor, out_path=args.out)

if __name__ == "__main__":
    main()
