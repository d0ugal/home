"""Add webcam model

Revision ID: 1923acffb84
Revises: 117cd76539b
Create Date: 2014-05-15 20:31:47.634183

"""

# revision identifiers, used by Alembic.
revision = '1923acffb84'
down_revision = '117cd76539b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'webcams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=True),
        sa.Column('url', sa.String(length=250), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_webcams_created_on', 'webcams', ['created_on'], unique=False)
    op.create_index('ix_webcams_name', 'webcams', ['name'], unique=True)


def downgrade():
    op.drop_index('ix_webcams_name', table_name='webcams')
    op.drop_index('ix_webcams_created_on', table_name='webcams')
    op.drop_table('webcams')
