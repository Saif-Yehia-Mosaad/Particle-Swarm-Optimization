# # ================================================================
# # PSO CLOUDLET PLACEMENT - TEAM PROJECT (7 members, equal division)
# # ================================================================
# # TEAM MEMBER 1 (Lines 1-44): Imports, config, data loading
# # ================================================================
# import pandas as pd
# import numpy as np
# import random

# # Set seeds for reproducibility - ensures same output every run
# np.random.seed(42)
# random.seed(42)

# # Read data from Excel file
# FILE_NAME = 'cloudlet_problem_dataset_full.xlsx'


# def load_data():

#     print("Loading data...")
#     try:
#         devices = pd.read_excel(
#             FILE_NAME, sheet_name='Devices').to_dict('records')
#         cloudlets = pd.read_excel(
#             FILE_NAME, sheet_name='Cloudlets').to_dict('records')
#     except Exception as e:
#         print(f"Error loading main sheets: {e}")
#         return [], [], []

#     # Try to load candidate points; if not found, generate dummy points for the code to work
#     try:
#         points = pd.read_excel(
#             FILE_NAME, sheet_name='CandidatePoints').to_dict('records')
#         print(f"Loaded {len(points)} candidate points.")
#     except:
#         print("Sheet 'CandidatePoints' not found. Generating grid points...")
#         points = []
#         for i in range(len(cloudlets) + 5):  # Sufficient number of locations
#             points.append({
#                 'point_id': f"P{i+1}",
#                 'x': random.uniform(0, 100),  # Default coordinates
#                 'y': random.uniform(0, 100),
#                 'location_cost': 100
#             })

#     return devices, cloudlets, points

# # ================================================================
# # TEAM MEMBER 2 (Lines 45-51): Distance calculation & helpers
# # ================================================================


# def calculate_distance(d, p):
#     return np.sqrt((d['x'] - p['x'])**2 + (d['y'] - p['y'])**2)

# # ================================================================
# # TEAM MEMBER 3 (Lines 52-112): Device-cloudlet assignment logic
# # ================================================================


# def smart_assignment(active_cloudlet_indices, cloudlets, devices, points):
#     """
#     This function attempts to connect each device to the nearest available cloudlet
#     instead of random guessing
#     """
#     total_cost = 0
#     total_latency = 0
#     device_assignments = {}  # Device_Index -> Cloudlet_Index

#     # Track capacity of each active cloudlet
#     current_load = {i: {'cpu': 0, 'ram': 0, 'storage': 0}
#                     for i in active_cloudlet_indices}

#     # 1. Calculate location operation costs
#     used_points_indices = set(active_cloudlet_indices.values())
#     for p_idx in used_points_indices:
#         total_cost += points[p_idx]['location_cost']

#     for c_idx in active_cloudlet_indices:
#         total_cost += cloudlets[c_idx]['placement_cost']

#     # 2. Attempt to connect devices (most important first)
#     unassigned_count = 0

#     for d_idx, device in enumerate(devices):
#         best_cloudlet = -1
#         best_latency = float('inf')

#         # Loop through all active cloudlets and check which can serve this device
#         for c_idx, p_idx in active_cloudlet_indices.items():
#             point = points[p_idx]
#             cloudlet = cloudlets[c_idx]

#             # 1. Distance condition (Coverage Radius)
#             dist = calculate_distance(device, point)
#             if dist > cloudlet['coverage_radius']:
#                 continue

#             # 2. Capacity condition (Capacity)
#             if (current_load[c_idx]['cpu'] + device['cpu_demand'] > cloudlet['cpu_capacity']) or \
#                (current_load[c_idx]['ram'] + device['ram_demand'] > cloudlet['ram_capacity']):
#                 continue

#             # If conditions are met, calculate latency (Latency)
#             latency = dist + cloudlet.get('activation_latency_ms', 0)

#             # Select the server that gives us the least latency
#             if latency < best_latency:
#                 best_latency = latency
#                 best_cloudlet = c_idx

#         # Record the result for this device
#         if best_cloudlet != -1:
#             device_assignments[d_idx] = best_cloudlet
#             total_latency += best_latency

#             # Update server capacity
#             current_load[best_cloudlet]['cpu'] += device['cpu_demand']
#             current_load[best_cloudlet]['ram'] += device['ram_demand']
#         else:
#             unassigned_count += 1  # Failed to connect device

#     return total_cost, total_latency, unassigned_count, device_assignments

# # ================================================================
# # TEAM MEMBER 4 (Lines 113-149): Objective function & fitness
# # ================================================================


# def objective_function(particle, cloudlets, devices, points):
#     """
#     Particle: List of numbers; each number represents the (location index) for the corresponding cloudlet
#     If the number >= number of locations, it means the cloudlet is (OFF/inactive)
#     """
#     num_points = len(points)
#     active_map = {}  # Cloudlet_ID -> Point_ID

#     # Convert particle to decision (which is active and where is it placed)
#     # Use Set to prevent placing two servers in the same location
#     used_locations = set()

#     for c_idx, val in enumerate(particle):
#         p_idx = int(round(val))

#         # If the value is valid and the location is not reserved
#         if 0 <= p_idx < num_points:
#             if p_idx not in used_locations:
#                 active_map[c_idx] = p_idx
#                 used_locations.add(p_idx)

#     # If no server is active, this is a very poor solution
#     if len(active_map) == 0:
#         return 1e9

#     # Use smart assignment logic to calculate cost
#     cost, latency, unassigned, _ = smart_assignment(
#         active_map, cloudlets, devices, points)

#     # Penalty function
#     # If there are unconnected devices, the penalty becomes very large
#     penalty = unassigned * 100000

#     fitness = (cost * 1.0) + (latency * 1.0) + penalty
#     return fitness

# # ================================================================
# # TEAM MEMBER 5 (Lines 150-186): PSO initialization & main loop
# # ================================================================


# def run_pso():
#     # 1. Load data
#     devices, cloudlets, points = load_data()
#     if not devices or not cloudlets:
#         return

#     num_cloudlets = len(cloudlets)
#     num_points = len(points)

#     # PSO Parameters
#     num_particles = 30
#     iterations = 100
#     w, c1, c2 = 0.5, 1.5, 1.5

#     # Particle: [Location_Index_for_Cloudlet_1, Location_Index_for_Cloudlet_2, ...]
#     # Range: 0 to num_points + 2 (to allow "OFF" state)
#     dim = num_cloudlets
#     upper_bound = num_points + 2

#     # Initialization
#     X = np.random.uniform(0, upper_bound, (num_particles, dim))
#     V = np.zeros((num_particles, dim))

#     Pbest = X.copy()
#     Pbest_obj = np.array([float('inf')] * num_particles)

#     Gbest = X[0].copy()
#     Gbest_obj = float('inf')

#     print("\nStarting Optimization (Smart PSO)...")

#     for t in range(iterations):
#         for i in range(num_particles):
#             # Fitness Calculation
#             fitness = objective_function(X[i], cloudlets, devices, points)

#             # Update Personal Best
#             if fitness < Pbest_obj[i]:
#                 Pbest_obj[i] = fitness
#                 Pbest[i] = X[i].copy()

#                 # Update Global Best
#                 if fitness < Gbest_obj:
#                     Gbest_obj = fitness
#                     Gbest = X[i].copy()

#         # Update Velocity & Position
#         r1, r2 = np.random.rand(dim), np.random.rand(dim)
#         V = w * V + c1 * r1 * (Pbest - X) + c2 * r2 * (Gbest - X)
#         X = X + V
#         X = np.clip(X, 0, upper_bound)  # Keep within bounds

#         if t % 10 == 0:
#             # Show progress every 10 iterations (flush to ensure immediate terminal output)
#             print(f"Iter {t}: Best Fitness = {Gbest_obj:.2f}", flush=True)

#     # ================================================================
#     # TEAM MEMBER 6 (Lines 187-256): Results extraction & display
#     # ================================================================
#     print("\n" + "="*50)
#     print("OPTIMIZATION COMPLETE")
#     print("="*50 + "\n")

#     # Retrieve details of the best solution
#     active_map = {}
#     used_locations = set()
#     for c_idx, val in enumerate(Gbest):
#         p_idx = int(round(val))
#         if 0 <= p_idx < num_points:
#             if p_idx not in used_locations:
#                 active_map[c_idx] = p_idx
#                 used_locations.add(p_idx)

#     cost, latency, unassigned, assignments = smart_assignment(
#         active_map, cloudlets, devices, points)

#     if unassigned == 0:
#         print(f"Status: VALID SOLUTION ✅")
#         print(f"Total Cost: {cost:.2f}")
#         print(f"Total Latency: {latency:.2f}")

#         print("\n--- Placed Cloudlets ---")
#         for c_idx, p_idx in active_map.items():
#             c_name = cloudlets[c_idx].get('cloudlet_id', c_idx)
#             p_name = points[p_idx].get('point_id', p_idx)
#             print(f"Cloudlet [{c_name}] at Location [{p_name}]")

#         print("\n--- Device Assignments ---")
#         print(f"{'Device':<10} {'-->':<5} {'Cloudlet':<10} {'Latency':<10}")
#         for d_idx, c_idx in assignments.items():
#             d_name = devices[d_idx].get('device_id', d_idx)
#             c_name = cloudlets[c_idx].get('cloudlet_id', c_idx)

#             # Recalculate exact latency for display
#             dist = calculate_distance(
#                 devices[d_idx], points[active_map[c_idx]])
#             lat = dist + cloudlets[c_idx].get('activation_latency_ms', 0)
#             print(f"{d_name:<10} {'-->':<5} {c_name:<10} {lat:.2f}")

#     else:
#         print(f"Status: INVALID ❌")
#         print(f"Unassigned Devices: {unassigned}")
#         print("Try increasing the number of cloudlets or coverage radius.")


# # ================================================================
# # TEAM MEMBER 7 (Lines 257-261): Main execution
# # ================================================================
# if __name__ == "__main__":
#     import sys
#     try:
#         run_pso()
#     finally:
#         sys.exit(0)
