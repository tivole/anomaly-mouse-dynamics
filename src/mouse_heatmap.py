import csv
import math
import numpy as np
import matplotlib.pyplot as plt

def read_mouse_data(log_file):
    data_by_monitor = {}
    with open(log_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue
            event_type = row[2].strip()
            if event_type == "MOVE":
                try:
                    x = float(row[3])
                    y = float(row[4])
                    monitor_index = int(row[1].strip())
                    if monitor_index not in data_by_monitor:
                        data_by_monitor[monitor_index] = {"xs": [], "ys": []}
                    data_by_monitor[monitor_index]["xs"].append(x)
                    data_by_monitor[monitor_index]["ys"].append(y)
                except ValueError:
                    continue
    for monitor in data_by_monitor:
        data_by_monitor[monitor]["xs"] = np.array(data_by_monitor[monitor]["xs"])
        data_by_monitor[monitor]["ys"] = np.array(data_by_monitor[monitor]["ys"])
    return data_by_monitor

def plot_heatmaps(data_by_monitor, bins=100):
    num_monitors = 1 # len(data_by_monitor)
    if num_monitors == 0:
        print("No MOVE events found in the log file.")
        return

    if num_monitors == 1:
        monitor_index = next(iter(data_by_monitor))
        xs = data_by_monitor[monitor_index]["xs"]
        ys = data_by_monitor[monitor_index]["ys"]
        plt.figure(figsize=(10, 6))
        hb = plt.hist2d(xs, ys, bins=bins, cmap='hot')
        # plt.colorbar(label='Event Count')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        # plt.title(f'Mouse Heatmap for Monitor {monitor_index}')
        plt.title('Mouse dynamics heatmap')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    else:
        n = num_monitors
        ncols = math.ceil(math.sqrt(n))
        nrows = math.ceil(n / ncols)
        fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 4))
        axes = axes.flatten() if n > 1 else [axes]
        
        for idx, monitor_index in enumerate(sorted(data_by_monitor.keys())):
            xs = data_by_monitor[monitor_index]["xs"]
            ys = data_by_monitor[monitor_index]["ys"]
            ax = axes[idx]
            hb = ax.hist2d(xs, ys, bins=bins, cmap='hot')
            ax.set_title(f'Monitor {monitor_index}')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.invert_yaxis()  # Invert y-axis.
            fig.colorbar(hb[3], ax=ax)
        
        for j in range(idx + 1, len(axes)):
            axes[j].axis('off')
        
        plt.tight_layout()
        plt.show()

def main():
    log_file = "mouse_telemetry.log"
    data_by_monitor = read_mouse_data(log_file)
    plot_heatmaps(data_by_monitor)

if __name__ == '__main__':
    main()
