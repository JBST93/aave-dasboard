from flask import Flask, request, render_template, redirect, url_for, flash, Response, send_from_directory,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple admin user (no database needed)
class AdminUser(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == os.getenv('ADMIN_USERNAME'):
        return AdminUser(user_id)
    return None

from scripts.stablecoin_yield import get_stablecoin_rates
from scripts.yields import get_rates

from scripts.eth_yield_api import get_ethereum_yields as eth_yield
from scripts.stablecoin_info_render import get_stablecoin_info_render
from scripts.get_project_info import get_projects
from projects.curve.pool_data import get_pools

from instances.Categories import create_predefined_categories
from instances.Projects import Project
from instances.YieldRate import YieldRate
from instances.Stablecoin import Stablecoin
from instances.TokenData import TokenData
from instances.MoneyMarketRate import MoneyMarketRate


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test_page():
    return "<h1>TEST WORKS!</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
            login_user(AdminUser(username))
            return redirect(url_for('admin_index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/robot.txt')
def render_robot():
    robots_content = """# robots.txt file for TokenDataView
            User-agent: *
            Disallow: /api/
            """
    return Response(robots_content, mimetype='text/plain')

@app.errorhandler(500)
def handle_500(e):
    import traceback
    print("500 ERROR:", traceback.format_exc())
    return f"<pre>Error: {traceback.format_exc()}</pre>", 500

@app.route('/admin')
@app.route('/admin/')
@login_required
def admin_index():
    try:
        search = request.args.get('search', '')
        if search:
            projects = Project.query.filter(
                (Project.protocol_name.ilike(f'%{search}%')) |
                (Project.token_ticker.ilike(f'%{search}%'))
            ).all()
        else:
            projects = Project.query.all()
        return render_template('admin/index.html', projects=projects)
    except Exception as e:
        import traceback
        print("ADMIN ERROR:", traceback.format_exc())
        return f"<pre>Error: {traceback.format_exc()}</pre>", 500

@app.route('/admin/add-project', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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


# ============ YIELD RATES ADMIN ============
@app.route('/admin/yield-rates')
@login_required
def admin_yield_rates():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 50

    query = YieldRate.query.order_by(YieldRate.timestamp.desc())
    if search:
        query = query.filter(
            (YieldRate.project.ilike(f'%{search}%')) |
            (YieldRate.market.ilike(f'%{search}%')) |
            (YieldRate.chain.ilike(f'%{search}%'))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/yield_rates.html', items=pagination.items, pagination=pagination)

@app.route('/admin/yield-rates/add', methods=['GET', 'POST'])
@login_required
def admin_add_yield_rate():
    if request.method == 'POST':
        item = YieldRate(
            market=request.form['market'],
            project=request.form['project'],
            information=request.form.get('information'),
            yield_rate_base=float(request.form['yield_rate_base']),
            yield_rate_reward=float(request.form['yield_rate_reward']) if request.form.get('yield_rate_reward') else None,
            yield_token_reward=request.form.get('yield_token_reward'),
            tvl=float(request.form.get('tvl', 0)),
            action=request.form.get('action'),
            chain=request.form['chain'],
            type=request.form['type'],
            smart_contract=request.form['smart_contract']
        )
        db.session.add(item)
        db.session.commit()
        flash('Yield Rate added successfully', 'success')
        return redirect(url_for('admin_yield_rates'))
    return render_template('admin/yield_rate_form.html', item=None)

@app.route('/admin/yield-rates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_yield_rate(id):
    item = YieldRate.query.get_or_404(id)
    if request.method == 'POST':
        item.market = request.form['market']
        item.project = request.form['project']
        item.information = request.form.get('information')
        item.yield_rate_base = float(request.form['yield_rate_base'])
        item.yield_rate_reward = float(request.form['yield_rate_reward']) if request.form.get('yield_rate_reward') else None
        item.yield_token_reward = request.form.get('yield_token_reward')
        item.tvl = float(request.form.get('tvl', 0))
        item.action = request.form.get('action')
        item.chain = request.form['chain']
        item.type = request.form['type']
        item.smart_contract = request.form['smart_contract']
        db.session.commit()
        flash('Yield Rate updated successfully', 'success')
        return redirect(url_for('admin_yield_rates'))
    return render_template('admin/yield_rate_form.html', item=item)

@app.route('/admin/yield-rates/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_yield_rate(id):
    item = YieldRate.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Yield Rate deleted successfully', 'success')
    return redirect(url_for('admin_yield_rates'))


# ============ STABLECOINS ADMIN ============
@app.route('/admin/stablecoins')
@login_required
def admin_stablecoins():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 50

    query = Stablecoin.query.order_by(Stablecoin.timestamp.desc())
    if search:
        query = query.filter(
            (Stablecoin.token.ilike(f'%{search}%')) |
            (Stablecoin.entity.ilike(f'%{search}%')) |
            (Stablecoin.chain.ilike(f'%{search}%'))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/stablecoins.html', items=pagination.items, pagination=pagination)

@app.route('/admin/stablecoins/add', methods=['GET', 'POST'])
@login_required
def admin_add_stablecoin():
    if request.method == 'POST':
        item = Stablecoin(
            token=request.form['token'],
            entity=request.form.get('entity'),
            price=float(request.form['price']) if request.form.get('price') else None,
            supply=float(request.form['supply']),
            circulating=float(request.form['circulating']) if request.form.get('circulating') else None,
            chain=request.form['chain'],
            pegged_against=request.form['pegged_against'],
            info=request.form['info']
        )
        db.session.add(item)
        db.session.commit()
        flash('Stablecoin added successfully', 'success')
        return redirect(url_for('admin_stablecoins'))
    return render_template('admin/stablecoin_form.html', item=None)

@app.route('/admin/stablecoins/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_stablecoin(id):
    item = Stablecoin.query.get_or_404(id)
    if request.method == 'POST':
        item.token = request.form['token']
        item.entity = request.form.get('entity')
        item.price = float(request.form['price']) if request.form.get('price') else None
        item.supply = float(request.form['supply'])
        item.circulating = float(request.form['circulating']) if request.form.get('circulating') else None
        item.chain = request.form['chain']
        item.pegged_against = request.form['pegged_against']
        item.info = request.form['info']
        db.session.commit()
        flash('Stablecoin updated successfully', 'success')
        return redirect(url_for('admin_stablecoins'))
    return render_template('admin/stablecoin_form.html', item=item)

@app.route('/admin/stablecoins/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_stablecoin(id):
    item = Stablecoin.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Stablecoin deleted successfully', 'success')
    return redirect(url_for('admin_stablecoins'))


# ============ TOKEN DATA ADMIN ============
@app.route('/admin/token-data')
@login_required
def admin_token_data():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 50

    query = TokenData.query.order_by(TokenData.timestamp.desc())
    if search:
        query = query.filter(TokenData.token.ilike(f'%{search}%'))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/token_data.html', items=pagination.items, pagination=pagination)

@app.route('/admin/token-data/add', methods=['GET', 'POST'])
@login_required
def admin_add_token_data():
    if request.method == 'POST':
        item = TokenData(
            token=request.form['token'],
            price=float(request.form['price']) if request.form.get('price') else None,
            price_source=request.form.get('price_source'),
            tot_supply=float(request.form['tot_supply']) if request.form.get('tot_supply') else None,
            circ_supply=float(request.form['circ_supply']) if request.form.get('circ_supply') else None,
            tvl=float(request.form['tvl']) if request.form.get('tvl') else None,
            revenue=float(request.form['revenue']) if request.form.get('revenue') else None
        )
        db.session.add(item)
        db.session.commit()
        flash('Token Data added successfully', 'success')
        return redirect(url_for('admin_token_data'))
    return render_template('admin/token_data_form.html', item=None)

@app.route('/admin/token-data/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_token_data(id):
    item = TokenData.query.get_or_404(id)
    if request.method == 'POST':
        item.token = request.form['token']
        item.price = float(request.form['price']) if request.form.get('price') else None
        item.price_source = request.form.get('price_source')
        item.tot_supply = float(request.form['tot_supply']) if request.form.get('tot_supply') else None
        item.circ_supply = float(request.form['circ_supply']) if request.form.get('circ_supply') else None
        item.tvl = float(request.form['tvl']) if request.form.get('tvl') else None
        item.revenue = float(request.form['revenue']) if request.form.get('revenue') else None
        db.session.commit()
        flash('Token Data updated successfully', 'success')
        return redirect(url_for('admin_token_data'))
    return render_template('admin/token_data_form.html', item=item)

@app.route('/admin/token-data/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_token_data(id):
    item = TokenData.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Token Data deleted successfully', 'success')
    return redirect(url_for('admin_token_data'))


# ============ MONEY MARKET RATES ADMIN ============
@app.route('/admin/money-market')
@login_required
def admin_money_market():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    per_page = 50

    query = MoneyMarketRate.query.order_by(MoneyMarketRate.timestamp.desc())
    if search:
        query = query.filter(
            (MoneyMarketRate.protocol.ilike(f'%{search}%')) |
            (MoneyMarketRate.token.ilike(f'%{search}%')) |
            (MoneyMarketRate.chain.ilike(f'%{search}%'))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/money_market.html', items=pagination.items, pagination=pagination)

@app.route('/admin/money-market/add', methods=['GET', 'POST'])
@login_required
def admin_add_money_market():
    if request.method == 'POST':
        import json
        collateral = request.form.get('collateral')
        try:
            collateral = json.loads(collateral) if collateral else None
        except:
            collateral = [collateral] if collateral else None

        item = MoneyMarketRate(
            protocol=request.form['protocol'],
            token=request.form['token'],
            collateral=collateral,
            liquidity_rate=float(request.form['liquidity_rate']),
            liquidity_reward_rate=float(request.form['liquidity_reward_rate']) if request.form.get('liquidity_reward_rate') else None,
            liquidity_reward_token=request.form.get('liquidity_reward_token'),
            borrow_rate=float(request.form['borrow_rate']),
            chain=request.form['chain'],
            tvl=float(request.form.get('tvl', 0))
        )
        db.session.add(item)
        db.session.commit()
        flash('Money Market Rate added successfully', 'success')
        return redirect(url_for('admin_money_market'))
    return render_template('admin/money_market_form.html', item=None)

@app.route('/admin/money-market/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_money_market(id):
    item = MoneyMarketRate.query.get_or_404(id)
    if request.method == 'POST':
        import json
        collateral = request.form.get('collateral')
        try:
            collateral = json.loads(collateral) if collateral else None
        except:
            collateral = [collateral] if collateral else None

        item.protocol = request.form['protocol']
        item.token = request.form['token']
        item.collateral = collateral
        item.liquidity_rate = float(request.form['liquidity_rate'])
        item.liquidity_reward_rate = float(request.form['liquidity_reward_rate']) if request.form.get('liquidity_reward_rate') else None
        item.liquidity_reward_token = request.form.get('liquidity_reward_token')
        item.borrow_rate = float(request.form['borrow_rate'])
        item.chain = request.form['chain']
        item.tvl = float(request.form.get('tvl', 0))
        db.session.commit()
        flash('Money Market Rate updated successfully', 'success')
        return redirect(url_for('admin_money_market'))
    return render_template('admin/money_market_form.html', item=item)

@app.route('/admin/money-market/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_money_market(id):
    item = MoneyMarketRate.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Money Market Rate deleted successfully', 'success')
    return redirect(url_for('admin_money_market'))


# Flask CLI Commands
@app.cli.command('init-db')
def init_db_command():
    """Create database tables and seed default data."""
    db.create_all()

    # Seed categories if empty
    from instances.Categories import Category
    if Category.query.count() == 0:
        categories = [
            "Blockchain", "Stablecoin", "ETH & equivalent", "BTC & equivalent",
            "Lending", "Yield Aggregator", "DEX", "Derivatives", "Liquid Staking",
            "NFT", "Bridges", "DeFi", "Oracles", "Gaming", "RWA", "Memecoin"
        ]
        for name in categories:
            db.session.add(Category(name=name))
        db.session.commit()
        print(f'Seeded {len(categories)} categories')

    print('Database initialized successfully!')


if __name__ == '__main__':
    app.run()
