"""Remove unique from projects

Revision ID: feea6c32a65f
Revises: 2ec2368dc9b7
Create Date: 2024-09-10 18:27:08.398496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feea6c32a65f'
down_revision = '2ec2368dc9b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_constraint('projects_protocol_name_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.create_unique_constraint('projects_protocol_name_key', ['protocol_name'])

    # ### end Alembic commands ###
