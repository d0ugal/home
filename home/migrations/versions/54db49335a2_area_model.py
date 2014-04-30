"""Add the Area model

Revision ID: 54db49335a2
Revises: 2367ebea90d
Create Date: 2014-04-20 13:43:33.248879

"""

# revision identifiers, used by Alembic.
revision = '54db49335a2'
down_revision = '2367ebea90d'

from datetime import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():

    connection = op.get_bind()

    op.create_table(
        'area',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_area_created_at', 'area', ['created_at'], unique=False)
    op.create_index('ix_area_name', 'area', ['name'], unique=True)
    op.add_column('device', sa.Column('area_id', sa.Integer()))

    # Create two hybrid tables that represent the new table and the old
    # device table with the new area_id column.
    area_migrator = sa.Table(
        'area',
        sa.MetaData(),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=True)
    )

    device_migrator = sa.Table(
        'device',
        sa.MetaData(),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=True),
        sa.Column('device_type', sa.Integer(), nullable=True),
        sa.Column('device_sub_type', sa.Integer(), nullable=True),
        sa.Column('device_id', sa.String(length=20), nullable=False),
        sa.Column('area_id', sa.Integer())
    )

    for device in connection.execute(device_migrator.select()):

        name = device.name

        connection.execute(
            area_migrator.insert()
            .values(name=name,
                    created_at=datetime.utcnow()))

        # After inserting, grab it back. We need to get the ID.
        r = connection.execute(
            area_migrator
            .select().where(
                area_migrator.c.name == name,
            ))

        area = r.first()

        # Update the data_point table to populate the new device_series_id.
        connection.execute(
            device_migrator.update().where(
                device_migrator.c.id == device.id
            ).values(
                area_id=area['id']
            )
        )

    # Ok, now its fully populated. Disable nulls on the col. If there are still
    # nulls we will get an error here, so its a good sanity check.
    op.alter_column('device', 'area_id', nullable=False)

    # Finally drop the old stuff as per the alembic generated code.
    op.drop_column('device', 'name')


def downgrade():
    op.create_index('ix_device_name', 'device', ['name'], unique=True)
    op.add_column('device', sa.Column('name', sa.VARCHAR(length=20),
                  nullable=True))
    op.drop_column('device', 'area_id')
    op.drop_index('ix_area_name', table_name='area')
    op.drop_index('ix_area_created_at', table_name='area')
    op.drop_table('area')
