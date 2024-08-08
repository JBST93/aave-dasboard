from flask import Flask, jsonify
import sys, os, json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
json_file_path = os.path.join(project_root, 'projects', 'projects.json')


from app import app

def get_projects():
    with app.app_context():
        try:
            with open(json_file_path, 'r') as file:
                projects = json.load(file)
                return jsonify(projects)
        except Exception as e:
            return (jsonify({"error": str(e)}), 500)
