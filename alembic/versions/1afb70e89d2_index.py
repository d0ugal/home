"""Index DataPoint.created_at

Revision ID: 1afb70e89d2
Revises: 43e49e93f5d
Create Date: 2014-04-12 15:36:18.025078

"""

# revision identifiers, used by Alembic.
revision = '1afb70e89d2'
down_revision = '43e49e93f5d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_data_point_created_at', 'data_point', ['created_at'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_data_point_created_at', table_name='data_point')
    ### end Alembic commands ###