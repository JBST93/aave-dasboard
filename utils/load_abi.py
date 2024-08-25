import os
import json
import sys

# Ensure the root directory is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_root)

from app import db
from instances.YieldRate import YieldRate as Data


def load_abi(project, abi_filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abi_path = os.path.join(script_dir, '..', "projects", project ,abi_filename)  # Adjust this line
    with open(abi_path) as f:
        try:
            return json.load(f)
        except FileNotFoundError:
            print(f"{abi_filename} file not found at {abi_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {abi_path}")
            sys.exit(1)
