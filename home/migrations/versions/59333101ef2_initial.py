"""Initial

Revision ID: 59333101ef2
Revises: None
Create Date: 2014-04-10 14:18:20.235516

"""

# revision identifiers, used by Alembic.
revision = '59333101ef2'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'device',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=True),
        sa.Column('device_type', sa.Integer(), nullable=True),
        sa.Column('device_sub_type', sa.Integer(), nullable=True),
        sa.Column('device_id', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('device_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'data_point',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('value', sa.Numeric(), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
        sa.ForeignKeyConstraint(['series_id'], ['series.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('data_point')
    op.drop_table('device')
    op.drop_table('series')
