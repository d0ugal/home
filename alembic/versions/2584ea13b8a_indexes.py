"""indexes

Revision ID: 2584ea13b8a
Revises: 25768ce6905
Create Date: 2014-04-20 09:23:42.942280

"""

# revision identifiers, used by Alembic.
revision = '2584ea13b8a'
down_revision = '25768ce6905'

from alembic import op


def upgrade():
    op.create_index('ix_data_point_device_series_id', 'data_point',
                    ['device_series_id'], unique=False)
    op.create_index('ix_data_point_value', 'data_point', ['value'],
                    unique=False)
    op.create_index('ix_device_created_at', 'device', ['created_at'],
                    unique=False)
    op.create_index('ix_device_device_sub_type', 'device', ['device_sub_type'],
                    unique=False)
    op.create_index('ix_device_device_type', 'device', ['device_type'],
                    unique=False)
    op.create_index('ix_device_name', 'device', ['name'], unique=True)
    op.create_index('ix_device_series_created_at', 'device_series',
                    ['created_at'], unique=False)
    op.create_index('ix_graph_name', 'graph', ['name'], unique=True)
    op.create_index('ix_series_created_at', 'series', ['created_at'],
                    unique=False)
    op.create_index('ix_series_name', 'series', ['name'], unique=True)


def downgrade():
    op.drop_index('ix_series_name', table_name='series')
    op.drop_index('ix_series_created_at', table_name='series')
    op.drop_index('ix_graph_name', table_name='graph')
    op.drop_index('ix_device_series_created_at', table_name='device_series')
    op.drop_index('ix_device_name', table_name='device')
    op.drop_index('ix_device_device_type', table_name='device')
    op.drop_index('ix_device_device_sub_type', table_name='device')
    op.drop_index('ix_device_created_at', table_name='device')
    op.drop_index('ix_data_point_value', table_name='data_point')
    op.drop_index('ix_data_point_device_series_id', table_name='data_point')
