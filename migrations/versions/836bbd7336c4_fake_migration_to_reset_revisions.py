"""Fake migration to reset revisions

Revision ID: 836bbd7336c4
Create Date: <date>
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '836bbd7336c4'
down_revision = None  # Add this line

branch_labels = None
depends_on = None

def upgrade():
    # No-op upgrade function
    pass

def downgrade():
    # Add a downgrade function, even if it's a no-op
    pass
