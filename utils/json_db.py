import json
import os

def read_data(file_path):
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def write_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)