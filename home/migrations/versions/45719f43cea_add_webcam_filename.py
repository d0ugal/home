"""Add webcam filename

Revision ID: 45719f43cea
Revises: 1923acffb84
Create Date: 2014-05-16 07:57:21.671458

"""

# revision identifiers, used by Alembic.
revision = '45719f43cea'
down_revision = '1923acffb84'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'webcams', sa.Column('filename', sa.String(length=20), nullable=True))
    op.create_index(
        op.f('ix_webcams_filename'), 'webcams', ['filename'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_webcams_filename'), table_name='webcams')
    op.drop_column('webcams', 'filename')
