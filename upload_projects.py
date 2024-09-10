import json
import os
from app import db, app
from instances.Projects import Project
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, 'projects.json')
projects_data = json.load(open(json_file_path))

with open(json_file_path, 'r') as file:
    projects_data = json.load(file)



def bulk_upload_projects(projects):
    for data in projects:
        project = Project(
            protocol_name=data.get('project'),
            token_ticker=data.get('token'),
            logo_url=data.get('logoUrl'),
            description=data.get('description'),
            category_main=data.get('business'),  # Mapping 'business' to 'category_main'
            website=data.get('website'),
            forum=data.get('forum'),
            token_decimals=data.get('decimals'),
            chain_main=None,  # You can adjust the mapping based on your needs
            contract_main=None,  # If available in your data, add it
            snapshot_name=None,  # Adjust if needed
            github_link=None,  # Adjust if needed
            alert=None,
            timestamp=datetime.now()
        )
        db.session.add(project)

    db.session.commit()
    print(f"{len(projects)} projects have been uploaded.")

with app.app_context():
    bulk_upload_projects(projects_data)
