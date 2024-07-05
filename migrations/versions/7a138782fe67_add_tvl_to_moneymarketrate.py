"""Add tvl  to MoneyMarketRate

Revision ID: 7a138782fe67
Revises: c37d67cd5d9e
Create Date: 2024-07-05 12:03:28.359106

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7a138782fe67'
down_revision = 'c37d67cd5d9e'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('money_market_rate', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tvl', sa.Float, nullable=True))

def downgrade():
    with op.batch_alter_table('money_market_rate', schema=None) as batch_op:
        batch_op.drop_column('tvl')
