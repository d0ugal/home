"""Add the user model

Revision ID: 490c5b501a3
Revises: 1e665b27760
Create Date: 2014-04-25 08:38:29.594656

"""

# revision identifiers, used by Alembic.
revision = '490c5b501a3'
down_revision = '1e665b27760'

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=20), nullable=True),
        sa.Column('password', sa.String(length=250), nullable=True),
        sa.Column('email', sa.String(length=50), nullable=True),
        sa.Column('registered_on', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_registered_on', 'users', ['registered_on'],
                    unique=False)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)


def downgrade():
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_registered_on', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
