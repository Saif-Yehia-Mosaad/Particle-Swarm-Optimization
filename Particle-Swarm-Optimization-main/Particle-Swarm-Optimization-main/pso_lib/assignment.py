from .utils import calculate_distance


#! member 4
def _assign_devices_to_cloudlets(active_cloudlet_indices, cloudlets, devices, points):
    total_latency = 0
    device_assignments = {}
    unassigned_count = 0

    #! Track capacity
    current_load = {i: {'cpu': 0, 'ram': 0, 'storage': 0}
                    for i in active_cloudlet_indices}

    for device_index, device in enumerate(devices):
        best_cloudlet = -1
        best_latency = float('inf')

        # * Check suitable cloudlets
        for cloudlet_index, location_index in active_cloudlet_indices.items():
            point = points[location_index]
            cloudlet = cloudlets[cloudlet_index]

            # * Distance
            dist = calculate_distance(device, point)
            if dist > cloudlet['coverage_radius']:
                continue

            # * Capacity
            if (current_load[cloudlet_index]['cpu'] + device['cpu_demand'] > cloudlet['cpu_capacity']) or \
               (current_load[cloudlet_index]['ram'] + device['ram_demand'] > cloudlet['ram_capacity']):
                continue

            # * Latency
            latency = dist + cloudlet.get('activation_latency_ms', 0)

            if latency < best_latency:
                best_latency = latency
                best_cloudlet = cloudlet_index

        #! save result for current device
        if best_cloudlet != -1:
            device_assignments[device_index] = best_cloudlet
            total_latency += best_latency

            # * Update Info ==> "Capacity"
            current_load[best_cloudlet]['cpu'] += device['cpu_demand']
            current_load[best_cloudlet]['ram'] += device['ram_demand']
        else:
            unassigned_count += 1

    return total_latency, unassigned_count, device_assignments


#! member 4
def _calculate_infrastructure_cost(active_cloudlet_indices, cloudlets, points):
    total_cost = 0
    used_points_indices = set(active_cloudlet_indices.values())
    for location_index in used_points_indices:
        total_cost += points[location_index]['location_cost']

    for cloudlet_index in active_cloudlet_indices:
        total_cost += cloudlets[cloudlet_index]['placement_cost']
    return total_cost


#! member 5
def smart_assignment(active_cloudlet_indices, cloudlets, devices, points):
    total_cost = _calculate_infrastructure_cost(
        active_cloudlet_indices, cloudlets, points)

    total_latency, unassigned_count, device_assignments = _assign_devices_to_cloudlets(
        active_cloudlet_indices, cloudlets, devices, points
    )

    return total_cost, total_latency, unassigned_count, device_assignments
