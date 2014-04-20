"""Graph model

Revision ID: 25768ce6905
Revises: 1afb70e89d2
Create Date: 2014-04-20 09:17:23.956372

"""

# revision identifiers, used by Alembic.
revision = '25768ce6905'
down_revision = '1afb70e89d2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'graph',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.Column('aggregator', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.drop_index('data_point_created_at_idx', table_name='data_point')
    op.drop_index('data_point_value_idx', table_name='data_point')
    op.add_column('series', sa.Column('graph_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('series', 'graph_id')
    op.create_index('data_point_value_idx', 'data_point', ['value'],
                    unique=False)
    op.create_index('data_point_created_at_idx', 'data_point', ['created_at'],
                    unique=False)
    op.drop_table('graph')
