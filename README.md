# Anomaly Mouse Dynamics Repository

This repository contains the reference implementation for the paper "Detection of Behavioural Baseline Deviation in Endpoint Usage through Mouse Dynamics Analysis". It provides tools to simulate, process, and analyse mouse movement telemetry for behavioural anomaly detection on endpoints.

## Repository Structure

```bash
├── .editorconfig           # Editor configuration
├── .gitignore              # Git ignore patterns
├── poetry.lock             # Locked Python dependencies
├── pyproject.toml          # Project configuration
├── README.md               # This file
├── images/                 # Sample heatmap and flowchart figures
├── notebooks/              # Jupyter notebooks for optimisation experiments
│   ├── clustering_optimisation.ipynb    # Clustering Methods Evaluation and Optimisation
│   └── comparison_optimisation.ipynb    # Comparison Methods Evaluation and Optimisation
└── src/                    # Source code and example data
    ├── mouse_heatmap.py            # Heatmap generation from raw telemetry
    ├── simulation_heatmap.py       # Synthetic mouse movement simulator
    ├── mouse_metrics.py            # Utility functions for metric calculations
    ├── mouse_movement_draw.py      # Visualisation of cursor trajectories
    ├── mouse_telemetry.log         # Sample raw telemetry log
    ├── results.json                # Results from clustering and comparison methods
    └── __init__.py                 # Python package marker
```

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To set up the environment:

```bash
# Clone the repository
git clone https://github.com/tivole/anomaly-mouse-dynamics.git
cd anomaly-mouse-dynamics

# Install dependencies via Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Usage

1. Simulate mouse dynamics data

```bash
python src/simulation_heatmap.py
```

Generates synthetic cursor trajectories and corresponding telemetry logs.

2. Generate heatmaps from telemetry data

```bash
python src/mouse_heatmap.py --input src/mouse_telemetry.log --output_dir images/
```

3. Optimisation and analysis of the methods:

```bash
jupyter notebook notebooks/clustering_optimisation.ipynb
jupyter notebook notebooks/comparison_optimisation.ipynb
```

Use these to benchmark and select clustering and comparison methods.

4. Visualisation

```bash
python src/mouse_movement_draw.py --input data/mouse_telemetry.log --out images/trajectory.png
```

Produces a plot of cursor movements, clicks, and scroll events.

## Citation

If you use this code in your research, please cite our paper (will be updated with actual details, once available):

```bibtex
@inproceedings{KNAsgarov2025,
  title={Detection of Behavioural Baseline Deviation in Endpoint Usage through Mouse Dynamics Analysis},
  author={},
  booktitle={},
  year={2025},
  publisher={}
}
```

