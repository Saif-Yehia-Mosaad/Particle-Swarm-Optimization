# PSO Cloudlet Placement Optimization

This project implements a **Particle Swarm Optimization (PSO)** algorithm to solve the Cloudlet Placement problem. It aims to find the optimal specific locations for cloudlets (edge servers) to minimize deployment costs and network latency for mobile devices.

## 👥 Team Responsibilities

- **Member 1**: Data Loading & Configuration (`data.py`, `config.py`)
- **Member 2**: Core PSO Optimizer (`optimizer.py`)
- **Member 3**: Objective Function (`objective.py`)
- **Member 4**: Core Logic & Utils (`utils.py`, `assignment.py` - device allocation - cost calc)
- **Member 5**: Business Logic & Costs & Reporting & Console Output (`reporting.py`,`assignment.py`, smart assignment)
- **Member 6**: GUI & Main Application (`gui_app.py`- init , `main.py`)
- **Member 7**: GUI & Main Application (`gui_app.py`- run , plot)

## 🚀 How to Run

### Graphical User Interface (GUI)

The recommended way to use the tool. Visualizes the optimization process.

```bash
python gui_app.py
```

### Command Line Interface (CLI)

For quick text-based results.

```bash
python main.py
```

## 📂 Project Structure

- **`pso_lib/`**: Contains the core logic library.
  - `optimizer.py`: The PSO algorithm implementation.
  - `objective.py`: The fitness function.
  - `assignment.py`: Logic for assigning devices to servers.
  - `data.py`: Data loading utilities.
- **`gui_app.py`**: The Tkinter + Matplotlib visualization tool.
- **`main.py`**: CLI entry point.

## ⚙️ Features

- **Smart Assignment**: Considers coverage radius, CPU/RAM capacity, and latency.
- **Visualization**: See devices, cloudlets, and connections on a 2D map.
- **Reproducibility**: Set seeds to get consistent results for analysis.
