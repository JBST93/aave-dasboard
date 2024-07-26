"""Add entity column to Stablecoin

Revision ID: a2b703c9e9b5
Revises: cacd02545397
Create Date: 2024-07-22 16:14:01.637573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'a2b703c9e9b5'
down_revision = 'cacd02545397'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current connection and inspector
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    # Get the list of columns in the 'stablecoin' table
    columns = [col['name'] for col in inspector.get_columns('stablecoin')]

    # Check if the 'entity' column already exists
    if 'entity' not in columns:
        # If it doesn't exist, add the 'entity' column
        with op.batch_alter_table('stablecoin', schema=None) as batch_op:
            batch_op.add_column(sa.Column('entity', sa.String(length=128), nullable=True))


def downgrade():
    with op.batch_alter_table('stablecoin', schema=None) as batch_op:
        batch_op.drop_column('entity')
