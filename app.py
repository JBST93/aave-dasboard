from flask import Flask, jsonify, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import humanize
from datetime import datetime
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

from scripts.stablecoin_yield import get_stablecoin_rates
from scripts.yields import get_rates

from scripts.eth_yield_api import get_ethereum_yields as eth_yield
from scripts.stablecoin_info_render import get_stablecoin_info_render
from scripts.get_project_info import get_projects
from projects.curve.pool_data import get_pools

@app.route('/robot.txt')
def render_robot():
    robots_content = """# robots.txt file for TokenDataView
            User-agent: *
            Disallow: /api/
            """
    return Response(robots_content, mimetype='text/plain')

@app.route('/api/projects',methods=["GET"])
def get_project_list():
    return get_projects()

@app.route('/api/stablecoin_yield_rates', methods=['GET'])
def liquidity_rates():
    return get_stablecoin_rates()

@app.route('/api/yield_rates', methods=['GET'])
def liquidity_rates():
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()
