"""empty message

Revision ID: 3b02dd36b3c
Revises: 45719f43cea
Create Date: 2014-06-14 13:12:43.544539

"""

# revision identifiers, used by Alembic.
revision = '3b02dd36b3c'
down_revision = '45719f43cea'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('webcams', 'filename')


def downgrade():
    op.add_column('webcams', sa.Column('filename', sa.VARCHAR(length=20),
                                       autoincrement=False, nullable=True))
