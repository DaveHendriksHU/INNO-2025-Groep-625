"""
Main script for running the agent-based model simulation.

This script initializes the simulation environment and runs it for a specified
number of years. It collects data for visualization and detailed household
information at the end of each simulation year.
"""

import random
import numpy as np
import time
from environment import Environment
import utilities
from shared_state import get_delay

import os
import glob

# Load configuration
config_id, config = utilities.choose_config()

# Global lists to store data from the simulation for potential use by an API or UI.
graphics_data = []  # Stores yearly aggregated data for charts/graphs.
households_data = []  # Stores detailed household information per year (updated yearly)

# Global pause flag
simulation_paused = False


def initialize_data_collection(model: Environment):
    save_folder = config['data_save_folder']
    os.makedirs(save_folder, exist_ok=True)

    existing_files = glob.glob(os.path.join(save_folder, "simulation_data_*.json"))
    run_number = len(existing_files) + 1
    file_name = os.path.join(save_folder, f"simulation_data_{run_number:03d}.json")

    model.setup_data_structure(file_name)

    return file_name


def toggle_simulation_pause():
    """
    Toggle the global pause state of the simulation.
    Returns:
        bool: The new paused state (True if paused, False if running).
    """
    global simulation_paused
    simulation_paused = not simulation_paused
    return simulation_paused


def is_simulation_paused():
    """
    Check if the simulation is currently paused.
    Returns:
        bool: True if paused, False otherwise.
    """
    return simulation_paused


def run_simulation(nr_households=10, nr_residents=10, simulation_years=30, seed=None):
    """
    Runs the agent-based model simulation.

    Initializes the model with the given parameters, runs it for the specified
    number of simulation years, and collects data.

    Args:
        nr_households (int): The number of households in the simulation.
        nr_residents (int): The total number of residents, distributed among households.
        simulation_years (int): The number of years the simulation will run.
        seed (int): Seed for random number generators for reproducibility.

    Returns:
        dict: A dictionary containing a message indicating simulation completion.
    """
    global graphics_data
    global households_data

    if seed is None:
        seed = random.randint(0, 2 ** 32 - 1)

    random.seed(seed)
    np.random.seed(seed)

    graphics_data.clear()
    households_data.clear()

    model = Environment(nr_households=nr_households, nr_residents=nr_residents)

    if config['collect_data']:
        file_name = initialize_data_collection(model)

    for year in range(simulation_years):
        while is_simulation_paused():
            time.sleep(1)

        print(f"=== Year {year + 1} ===")
        print("Current Environment State (begin):")
        print(model)

        data = model.collect_start_of_year_data(year + 1)
        model.step()

        print(f"\nEnd of Year {year + 1}:")
        for package_name, count in model.decided_residents_this_step_per_package.items():
            print(f"  Decisions this year for {package_name}: {count}")

        print("  Current Environment State (end):")
        print(model)
        print("-" * 40)

        model.collect_end_of_year_data(data)
        graphics_data.append(data)

        # Export data to JSON file if configured
        if config['collect_data']:
            model.export_data(file_name, year + 1)

        # Update household data (per year)
        households_data.clear()
        households_data.extend(model.collect_household_information())

        # Wait before next simulation year
        time.sleep(get_delay())


if __name__ == "__main__":
    simulation_result = run_simulation(
        config['nr_households'],
        config['nr_residents'],
        config['simulation_years'],
        config['seed']
    )