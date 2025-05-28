import numpy as np
import matplotlib.pyplot as plt

def simulate_mouse_path(state_params, width, height):
    if "initial_bias" in state_params:
        bias = state_params["initial_bias"]
        bias_std = state_params.get("bias_std", 50)
        x = int(np.clip(np.random.normal(bias[0], bias_std), 0, width-1))
        y = int(np.clip(np.random.normal(bias[1], bias_std), 0, height-1))
    else:
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
    
    angle = np.random.uniform(0, 2 * np.pi)
    events = []
    
    for _ in range(state_params["path_length"]):
        events.append((x, y))
        angle += np.random.normal(0, state_params.get("angle_variance", 0.1))
        if np.random.rand() < state_params.get("drift_probability", 0.05):
            if "drift_target" in state_params:
                target_x, target_y = state_params["drift_target"]
                desired_angle = np.arctan2(target_y - y, target_x - x)
                angle = (angle + desired_angle) / 2
        step = np.random.uniform(state_params.get("step_min", 1), state_params.get("step_max", 10))
        x += int(step * np.cos(angle))
        y += int(step * np.sin(angle))
        
        if "confined_region" in state_params:
            region = state_params["confined_region"]
            x = max(region[0], min(x, region[2]))
            y = max(region[1], min(y, region[3]))
        else:
            x = max(0, min(x, width-1))
            y = max(0, min(y, height-1))
    return events

def simulate_minute_heatmap(state_params, width, height, scale):
    all_events = []
    for _ in range(state_params["num_paths"]):
        events = simulate_mouse_path(state_params, width, height)
        all_events.extend(events)
    
    out_width = width // scale
    out_height = height // scale
    heatmap = np.zeros((out_height, out_width), dtype=float)
    
    for (x, y) in all_events:
        bin_x = int(x // scale)
        bin_y = int(y // scale)
        if 0 <= bin_x < out_width and 0 <= bin_y < out_height:
            heatmap[bin_y, bin_x] += 1
    
    max_val = heatmap.max()
    if max_val > 0:
        heatmap = heatmap / max_val
    return heatmap

def simulate_heatmap_series(total_minutes, timeline, width, height, scale):
    series = []
    for minute in range(total_minutes):
        state_label = None
        state_params = None
        for (start, end, label, params) in timeline:
            if start <= minute < end:
                state_label = label
                state_params = params
                break
        if state_params is None:
            state_params = {"num_paths": 10, "path_length": 500, "angle_variance": 0.1,
                            "step_min": 1, "step_max": 8, "drift_probability": 0.05}
            state_label = "default"
        heatmap = simulate_minute_heatmap(state_params, width, height, scale)
        series.append((minute, state_label, heatmap))
    return series

def plot_heatmap(heatmap, title="Simulated Heatmap"):
    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap, cmap="hot", origin="upper")
    plt.title(title)
    plt.xlabel("X bins")
    plt.ylabel("Y bins")
    plt.colorbar(label="Normalized Movement Count (0.0 to 1.0)")
    plt.show()

def main():
    width, height = 2560, 1440
    scale = 40

    state_A = {
        "num_paths": 20,
        "path_length": 800,
        "angle_variance": 0.2,
        "step_min": 2,
        "step_max": 8,
        "drift_probability": 0.1,
        "drift_target": (width // 2, height // 2),
        "initial_bias": (width // 2, height // 2),
        "bias_std": 100
    }
    
    state_B = {
        "num_paths": 15,
        "path_length": 1000,
        "angle_variance": 0.1,
        "step_min": 1,
        "step_max": 5,
        "drift_probability": 0.05,
        "confined_region": (width // 4, height // 4, width // 2, height // 2),
        "initial_bias": (width // 3, height // 3),
        "bias_std": 50
    }
    
    state_C = {
        "num_paths": 25,
        "path_length": 600,
        "angle_variance": 0.5,
        "step_min": 3,
        "step_max": 12,
        "drift_probability": 0.2,
        "drift_target": (int(width * 0.75), int(height * 0.75)),
        "initial_bias": (width // 2, height // 2),
        "bias_std": 150
    }

    state_D = {
        "num_paths": 10,
        "path_length": 400,
        "angle_variance": 0.3,
        "step_min": 2,
        "step_max": 6,
        "drift_probability": 0.1,
        "drift_target": (width // 4, height // 4),
        "initial_bias": (width // 4, height // 4),
        "bias_std": 80
    }

    state_E = {
        "num_paths": 50,
        "path_length": 500,
        "angle_variance": 0.8,
        "step_min": 3,
        "step_max": 4,
        "drift_probability": 0.3,
        "drift_target": (int(width * 0.35), int(height * 0.25)),
        "initial_bias": (width // 2, height // 2),
        "bias_std": 50
    }

    state_F = {
        "num_paths": 30,
        "path_length": 700,
        "angle_variance": 0.4,
        "step_min": 1,
        "step_max": 2,
        "drift_probability": 0.15,
        "drift_target": (int(width * 0.8), int(height * 0.8)),
        "initial_bias": (width // 2, height // 2),
        "bias_std": 100
    }
    
    timeline = [
        (0, 30, "State A", state_A),
        (30, 90, "State B", state_B),
        (90, 120, "State C", state_C),
        (120, 150, "State D", state_D),
        (150, 180, "State E", state_E),
        (180, 210, "State F", state_F),
    ]
    
    total_minutes = 210 
    series = simulate_heatmap_series(total_minutes, timeline, width, height, scale)

    sample_minutes = [185, 195, 205]
    for minute, state_label, heatmap in series:
        if minute in sample_minutes:
            plot_heatmap(heatmap, title=f"Minute {minute} - {state_label}")
    
    for minute, state_label, _ in series:
        print(f"Minute {minute}: {state_label}")

if __name__ == '__main__':
    main()
