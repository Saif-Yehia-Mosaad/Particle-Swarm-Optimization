import numpy as np
from .objective import objective_function

#! member 2 ===> Ismael


def execute_pso(devices, cloudlets, points, num_particles=30, iterations=100, inertia_weight=0.5, c1=1.5, social_coeff=1.5):
    if not devices or not cloudlets:
        return None, None

    num_cloudlets = len(cloudlets)
    num_points = len(points)

    #! more index for  (OFF state & flexibility)
    dim = num_cloudlets
    upper_bound = num_points + 2

    # * Initialize
    positions = np.random.uniform(0, upper_bound, (num_particles, dim))
    velocities = np.zeros((num_particles, dim))

    personal_best_positions = positions.copy()
    personal_best_scores = np.array([float('inf')] * num_particles)

    global_best_position = positions[0].copy()
    global_best_score = float('inf')

    print("\nStarting Optimization (Smart PSO)...")

    for t in range(iterations):
        for i in range(num_particles):
            #! Fitness
            fitness = objective_function(
                positions[i], cloudlets, devices, points)

            #! Update Personal Best
            if fitness < personal_best_scores[i]:
                personal_best_scores[i] = fitness
                personal_best_positions[i] = positions[i].copy()

            #! Update Global Best
            if fitness < global_best_score:
                global_best_score = fitness
                global_best_position = positions[i].copy()

        cognitive_random, social_random = np.random.rand(
            dim), np.random.rand(dim)
        velocities = inertia_weight * velocities + c1 * cognitive_random * (personal_best_positions - positions) + \
            social_coeff * social_random * (global_best_position - positions)
        positions = positions + velocities
        positions = np.clip(positions, 0, upper_bound)

        if t % 10 == 0:

            #! progress every 10 iterations
            print(
                f"Iter {t}: Best Fitness = {global_best_score:.2f}", flush=True)

    return global_best_position, global_best_score
