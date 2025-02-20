"""initial migration

Revision ID: d2023_initial_migration
Revises:
Create Date: 2023-12-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic
revision = 'd2023_initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create stablecoin table
    op.create_table(
        'stablecoin',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(50), nullable=False),
        sa.Column('entity', sa.String(50), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('supply', sa.Float(), nullable=False),
        sa.Column('circulating', sa.Float(), nullable=True),
        sa.Column('chain', sa.String(20), nullable=False),
        sa.Column('pegged_against', sa.String(20), nullable=False),
        sa.Column('info', sa.String(20), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('protocol_name', sa.String(100), nullable=False),
        sa.Column('token_ticker', sa.String(20), nullable=False),
        sa.Column('logo_url', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category_main', sa.String(50), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('forum', sa.String(255), nullable=True),
        sa.Column('alert', sa.Text(), nullable=True),
        sa.Column('token_decimals', sa.Integer(), nullable=True),
        sa.Column('chain_main', sa.String(50), nullable=True),
        sa.Column('contract_main', sa.String(100), nullable=True),
        sa.Column('snapshot_name', sa.String(100), nullable=True),
        sa.Column('github_link', sa.String(255), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create money_market_rate table
    op.create_table(
        'money_market_rate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('protocol', sa.String(50), nullable=False),
        sa.Column('token', sa.String(50), nullable=False),
        sa.Column('collateral', JSONB(), nullable=True),
        sa.Column('liquidity_rate', sa.Float(), nullable=False),
        sa.Column('liquidity_reward_rate', sa.Float(), nullable=True),
        sa.Column('liquidity_reward_token', sa.String(50), nullable=True),
        sa.Column('borrow_rate', sa.Float(), nullable=False),
        sa.Column('chain', sa.String(20), nullable=False),
        sa.Column('tvl', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create token_data table
    op.create_table(
        'token_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(100), nullable=False),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('price_source', sa.String(100), nullable=True),
        sa.Column('tot_supply', sa.Float(), nullable=True),
        sa.Column('circ_supply', sa.Float(), nullable=True),
        sa.Column('tvl', sa.Float(), nullable=True),
        sa.Column('revenue', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create yield_rate table
    op.create_table(
        'yield_rate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('market', sa.String(100), nullable=False),
        sa.Column('project', sa.String(100), nullable=False),
        sa.Column('information', sa.String(200), nullable=True),
        sa.Column('yield_rate_base', sa.Float(), nullable=False),
        sa.Column('yield_rate_reward', sa.Float(), nullable=True),
        sa.Column('yield_token_reward', sa.String(50), nullable=True),
        sa.Column('tvl', sa.Float(), nullable=False),
        sa.Column('action', sa.String(150), nullable=True),
        sa.Column('chain', sa.String(20), nullable=False),
        sa.Column('type', sa.String(150), nullable=False),
        sa.Column('smart_contract', sa.String(150), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop tables in reverse order of creation
    op.drop_table('yield_rate')
    op.drop_table('token_data')
    op.drop_table('money_market_rate')
    op.drop_table('projects')
    op.drop_table('stablecoin')
    op.drop_table('categories')
