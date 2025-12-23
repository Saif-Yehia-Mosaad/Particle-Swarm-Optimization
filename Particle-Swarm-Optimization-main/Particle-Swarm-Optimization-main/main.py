import sys
from pso_lib.config import init_seeds
from pso_lib.data import load_data
from pso_lib.optimizer import execute_pso
from pso_lib.reporting import print_results

#! member 6


def main():
    try:
        #! Initialize
        init_seeds()

        #! Load Data
        devices, cloudlets, points = load_data()

        #! Run Optimization
        Gbest, _ = execute_pso(devices, cloudlets, points)

        #! Display Results
        print_results(Gbest, devices, cloudlets, points)

    except KeyboardInterrupt:
        print("\nOptimization interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
