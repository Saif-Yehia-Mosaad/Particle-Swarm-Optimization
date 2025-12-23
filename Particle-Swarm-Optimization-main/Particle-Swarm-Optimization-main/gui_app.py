import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from pso_lib.data import load_data
from pso_lib.optimizer import execute_pso
from pso_lib.assignment import smart_assignment

#! member 6


class PSOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSO Cloudlet Placement")
        self.root.geometry("900x700")

        controls = ttk.Frame(root, padding=10)
        controls.pack(fill=tk.X)

        ttk.Label(controls, text="Particles").pack(side=tk.LEFT)
        self.particles = tk.IntVar(value=30)
        ttk.Entry(controls, width=5, textvariable=self.particles).pack(
            side=tk.LEFT, padx=5)

        ttk.Label(controls, text="Iterations").pack(side=tk.LEFT)
        self.iterations = tk.IntVar(value=50)
        ttk.Entry(controls, width=5, textvariable=self.iterations).pack(
            side=tk.LEFT, padx=5)

        ttk.Button(
            controls,
            text="Run PSO",
            command=self.run_pso
        ).pack(side=tk.LEFT, padx=20)

        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #! member 7

    def run_pso(self):
        try:
            np.random.seed(42)
            random.seed(42)

            devices, cloudlets, points = load_data()
            if not devices or not cloudlets:
                messagebox.showerror("Error", "Failed to load data")
                return

            Gbest, Gbest_val = execute_pso(
                devices,
                cloudlets,
                points,
                num_particles=self.particles.get(),
                iterations=self.iterations.get()
            )

            self.plot_result(Gbest, devices, cloudlets, points)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_result(self, Gbest, devices, cloudlets, points):
        self.ax.clear()

        active_map = {}
        used_locations = set()
        num_points = len(points)

        for c_idx, val in enumerate(Gbest):
            p_idx = int(round(val))
            if 0 <= p_idx < num_points and p_idx not in used_locations:
                active_map[c_idx] = p_idx
                used_locations.add(p_idx)

        cost, latency, _, assignments = smart_assignment(
            active_map, cloudlets, devices, points
        )

        self.ax.scatter(
            [p['x'] for p in points],
            [p['y'] for p in points],
            marker='x',
            alpha=0.4,
            label="Candidate Points"
        )

        self.ax.scatter(
            [d['x'] for d in devices],
            [d['y'] for d in devices],
            label="Devices"
        )

        cx = [points[p]['x'] for p in active_map.values()]
        cy = [points[p]['y'] for p in active_map.values()]
        self.ax.scatter(cx, cy, marker='s', label="Active Cloudlets")

        for d_idx, c_idx in assignments.items():
            d = devices[d_idx]
            p = points[active_map[c_idx]]
            self.ax.plot([d['x'], p['x']], [d['y'], p['y']],
                         linestyle='--', alpha=0.3)

        self.ax.set_title(f"Cost: {cost:.1f} | Latency: {latency:.1f}")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    PSOApp(root)
    root.mainloop()
