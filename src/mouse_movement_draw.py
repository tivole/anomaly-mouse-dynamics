import csv
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt

LOG_FILE = "mouse_telemetry.log"

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

def plot_all_events(moves, clicks, scrolls, monitor_index):
    fig, ax = plt.subplots(figsize=(10,6), dpi=120)

    mov_line, = ax.plot(
        moves[:,0], moves[:,1],
        linewidth=2, alpha=0.3, color='blue',
        label='Movement'
    )

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
    # ax.set_title(f'Mouse Events on Monitor {monitor_index}')
    ax.set_title('Mouse dynamics')
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
    plt.show()

if __name__ == "__main__":
    monitors = read_mouse_data(LOG_FILE)
    data = monitors["1"]
    plot_all_events(
        np.array(data["moves"]),
        np.array(data["clicks"]),
        np.array(data["scrolls"]),
        monitor_index=1
    )
