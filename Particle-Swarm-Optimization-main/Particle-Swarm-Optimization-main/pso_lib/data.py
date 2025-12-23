import pandas as pd
import random
from .config import FILE_NAME

#! member 1


def load_data():
    print("Loading data...")
    try:
        devices = pd.read_excel(
            FILE_NAME, sheet_name='Devices').to_dict('records')
        cloudlets = pd.read_excel(
            FILE_NAME, sheet_name='Cloudlets').to_dict('records')
    except Exception as e:
        print(f"Error loading main sheets: {e}")
        return [], [], []

    #! reading  or Generate candidate points in null "Case"
    try:
        points = pd.read_excel(
            FILE_NAME, sheet_name='CandidatePoints').to_dict('records')
        print(f"Loaded {len(points)} candidate points.")
    except:
        print("Sheet 'CandidatePoints' not found. Generating grid points...")
        points = []
        for i in range(len(cloudlets) + 5):
            points.append({
                'point_id': f"P{i+1}",
                'x': random.uniform(0, 100),
                'y': random.uniform(0, 100),
                'location_cost': 100
            })

    return devices, cloudlets, points
