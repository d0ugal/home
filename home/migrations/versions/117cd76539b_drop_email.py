"""Remove the user email, we don't need that.

Revision ID: 117cd76539b
Revises: 490c5b501a3
Create Date: 2014-04-25 09:14:52.907017

"""

# revision identifiers, used by Alembic.
revision = '117cd76539b'
down_revision = '490c5b501a3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('users', 'email')


def downgrade():
    op.add_column(
        'users', sa.Column('email', sa.VARCHAR(length=50), nullable=True))
