"""empty message

Revision ID: bb9da1ffdd9e
Revises: 36a02077fdec
Create Date: 2024-07-26 15:03:27.271347

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'bb9da1ffdd9e'
down_revision = '36a02077fdec'
branch_labels = None
depends_on = None


def upgrade():
    # Get the current connection and inspector
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    with op.batch_alter_table('money_market_rate', schema=None) as batch_op:
        batch_op.alter_column('collateral',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=True)

    with op.batch_alter_table('stablecoin', schema=None) as batch_op:
        batch_op.alter_column('entity',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('chain',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               existing_nullable=False)

        # Check and drop columns if they exist
        columns = [col['name'] for col in inspector.get_columns('stablecoin')]
        if 'type' in columns:
            batch_op.drop_column('type')
        if 'pegged_to' in columns:
            batch_op.drop_column('pegged_to')
        if 'project' in columns:
            batch_op.drop_column('project')

    with op.batch_alter_table('yield_rate', schema=None) as batch_op:
        batch_op.alter_column('market',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('project',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('information',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('type',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=150),
               existing_nullable=False)


def downgrade():
    with op.batch_alter_table('yield_rate', schema=None) as batch_op:
        batch_op.alter_column('type',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('information',
               existing_type=sa.String(length=200),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=True)
        batch_op.alter_column('project',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('market',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('stablecoin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('project', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('pegged_to', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('type', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.alter_column('chain',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('entity',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    with op.batch_alter_table('money_market_rate', schema=None) as batch_op:
        batch_op.alter_column('collateral',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=True)
