from .assignment import smart_assignment

#! member 3 ==> Saif


def objective_function(particle, cloudlets, devices, points):

    num_points = len(points)
    active_map = {}

    used_locations = set()

    for cloudlet_index, location_value in enumerate(particle):
        location_index = int(round(location_value))

        if 0 <= location_index < num_points:
            if location_index not in used_locations:
                active_map[cloudlet_index] = location_index
                used_locations.add(location_index)

    if len(active_map) == 0:
        return 1e9

    # * Calc cost
    cost, latency, unassigned, _ = smart_assignment(
        active_map, cloudlets, devices, points)

    #! Penalty
    penalty = unassigned * 100000
    #! fitness
    fitness = (cost * 1.0) + (latency * 1.0) + penalty
    return fitness
