from .assignment import smart_assignment
from .utils import calculate_distance

#! member 5


def print_results(Gbest, devices, cloudlets, points):
    if Gbest is None:
        return

    num_points = len(points)

    print("\n" + "="*50)
    print("OPTIMIZATION COMPLETE")
    print("="*50 + "\n")

    #! Best soultion
    active_map = {}
    used_locations = set()
    for cloudlet_idx, location_value in enumerate(Gbest):
        location_index = int(round(location_value))
        if 0 <= location_index < num_points:
            if location_index not in used_locations:
                active_map[cloudlet_idx] = location_index
                used_locations.add(location_index)

    cost, latency, unassigned, assignments = smart_assignment(
        active_map, cloudlets, devices, points)

    if unassigned == 0:
        print(f"Status: VALID SOLUTION ✅")
        print(f"Total Cost: {cost:.2f}")
        print(f"Total Latency: {latency:.2f}")

        print("\n--- Placed Cloudlets ---")
        for cloudlet_idx, location_idx in active_map.items():
            cloudlets_name = cloudlets[cloudlet_idx].get(
                'cloudlet_id', cloudlet_idx)
            Location_name = points[location_idx].get('point_id', location_idx)
            print(f"Cloudlet [{cloudlets_name}] at Location [{Location_name}]")

        print("\n--- Device Assignments ---")
        print(f"{'Device':<10} {'-->':<5} {'Cloudlet':<10} {'Latency':<10}")
        for device_idx, cloudlet_idx in assignments.items():
            device_name = devices[device_idx].get('device_id', device_idx)
            cloudlet_name = cloudlets[cloudlet_idx].get(
                'cloudlet_id', cloudlet_idx)

            dist = calculate_distance(
                devices[device_idx], points[active_map[cloudlet_idx]])
            lat = dist + \
                cloudlets[cloudlet_idx].get('activation_latency_ms', 0)
            print(f"{device_name:<10} {'-->':<5} {cloudlet_name:<10} {lat:.2f}")

    else:
        print(f"Status: INVALID ❌")
        print(f"Unassigned Devices: {unassigned}")
        print("Try increasing the number of cloudlets or coverage radius.")
