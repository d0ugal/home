"""Add graph description

Revision ID: 2367ebea90d
Revises: 2584ea13b8a
Create Date: 2014-04-20 11:21:00.657168

"""

# revision identifiers, used by Alembic.
revision = '2367ebea90d'
down_revision = '2584ea13b8a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('graph', sa.Column('description', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('graph', 'description')
