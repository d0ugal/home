"""Allow devices with no area_id.

Revision ID: 1e665b27760
Revises: 54db49335a2
Create Date: 2014-04-20 16:32:55.982893

"""

# revision identifiers, used by Alembic.
revision = '1e665b27760'
down_revision = '54db49335a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('device', 'area_id', existing_type=sa.INTEGER(),
                    nullable=True)


def downgrade():
    op.alter_column('device', 'area_id', existing_type=sa.INTEGER(),
                    nullable=False)
