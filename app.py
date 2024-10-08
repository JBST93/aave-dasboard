from flask import Flask, request, render_template, redirect, url_for, flash, Response, send_from_directory,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

from scripts.stablecoin_yield import get_stablecoin_rates
from scripts.yields import get_rates

from scripts.eth_yield_api import get_ethereum_yields as eth_yield
from scripts.stablecoin_info_render import get_stablecoin_info_render
from scripts.get_project_info import get_projects
from projects.curve.pool_data import get_pools

from instances.Categories import create_predefined_categories
from instances.Projects import Project


@app.route('/robot.txt')
def render_robot():
    robots_content = """# robots.txt file for TokenDataView
            User-agent: *
            Disallow: /api/
            """
    return Response(robots_content, mimetype='text/plain')

@app.route('/admin')
@app.route('/admin/')
def admin_index():
    search = request.args.get('search', '')
    if search:
        projects = Project.query.filter(
            (Project.protocol_name.ilike(f'%{search}%')) |
            (Project.token_ticker.ilike(f'%{search}%'))
        ).all()
    else:
        projects = Project.query.all()
    return render_template('admin/index.html', projects=projects)

@app.route('/admin/add-project', methods=['GET', 'POST'])
def admin_add_project():
    if request.method == 'POST':
        new_project = Project(
            protocol_name=request.form['protocol_name'],
            token_ticker=request.form['token_ticker'],
            logo_url=request.form['logo_url'],
            description=request.form['description'],
            category_main=request.form['category_main'],
            website=request.form['website'],
            forum=request.form['forum'],
            alert=request.form['alert'],
            token_decimals=int(request.form['token_decimals']),
            chain_main=request.form['chain_main'],
            contract_main=request.form['contract_main'],
            snapshot_name=request.form['snapshot_name'],
            github_link=request.form['github_link']
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully', 'success')
        return redirect(url_for('admin_index'))
    return render_template('admin/add_project.html')


@app.route('/admin/edit-project/<int:id>', methods=['GET', 'POST'])
def admin_edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.protocol_name = request.form['protocol_name']
        project.token_ticker = request.form['token_ticker']
        project.logo_url = request.form['logo_url']
        project.description = request.form['description']
        project.category_main = request.form['category_main']
        project.website = request.form['website'] or None
        project.forum = request.form['forum'] or None
        project.alert = request.form['alert']
        project.token_decimals = int(request.form['token_decimals'] or 0)
        project.chain_main = request.form['chain_main']
        project.contract_main = request.form['contract_main']
        project.snapshot_name = request.form['snapshot_name']
        project.github_link = request.form['github_link'] or None
        db.session.commit()
        flash('Project updated successfully', 'success')
        return redirect(url_for('admin_index'))
    return render_template('admin/edit_project.html', project=project)


@app.route('/admin/delete-project/<int:id>', methods=['POST'])
def admin_delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully', 'success')
    return redirect(url_for('admin_index'))


@app.route('/api/projects', methods=['GET'])
def get_project_list():
    return get_projects()

@app.route('/api/stablecoin_yield_rates', methods=['GET'])
def liquidity_rates():
    return get_stablecoin_rates()

@app.route('/api/yield_rates', methods=['GET'])
def all_rates():
    return get_rates()

@app.route('/api/eth_yields', methods=['GET'])
def eth_rate():
    return eth_yield()

@app.route('/api/stablecoin_info', methods=['GET'])
def stablecoin_info():
    return get_stablecoin_info_render()

@app.route('/api/curve-pools', methods=['GET'])
def pools_route():
    return get_pools()


if __name__ == '__main__':
    app.run()
