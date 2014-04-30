"""M2M Change

Revision ID: 43e49e93f5d
Revises: 59333101ef2
Create Date: 2014-04-10 15:36:40.970441

"""

# revision identifiers, used by Alembic.
revision = '43e49e93f5d'
down_revision = '59333101ef2'

from datetime import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():

    connection = op.get_bind()

    # Create the device_series table as per the default alembic generated code.
    op.create_table(
        'device_series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['device_id'], ['device.id'], ),
        sa.ForeignKeyConstraint(['series_id'], ['series.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('series_id', 'device_id', name='_series_device_uc')
    )

    # Add the relation to the new table in data_point, but remove the
    # nullable=False parameter. We need to allow nulls initially.
    op.add_column('data_point', sa.Column('device_series_id', sa.Integer()))

    # Create two hybrid tables that represent the new table and the old
    # data_point table with the new relationship column.
    data_point_migrator = sa.Table(
        'data_point',
        sa.MetaData(),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('value', sa.Numeric(), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('device_series_id', sa.Integer(), nullable=True),
    )

    device_series_migrator = sa.Table(
        'device_series',
        sa.MetaData(),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
    )

    # We know the unique constraint on device_services, so store them as we go
    # to make things a bit faster.
    seen_device_series = {}

    # Iterate through all of the data points. We want to extract the relation
    # on data_point to series and device and put it in the new device_series
    # table.
    for data_point in connection.execute(data_point_migrator.select()):

        # Pull the data from data_point.
        s_id = data_point.series_id
        d_id = data_point.device_id

        # Insert into device_series if it doesn't already exist.
        if (s_id, d_id) not in seen_device_series:

            # Simple insert, just use utcnow - we don't care much about that
            # it will be more useful for future inserts.
            connection.execute(
                device_series_migrator.insert()
                .values(series_id=s_id, device_id=d_id,
                        created_at=datetime.utcnow()))

            # After inserting, grab it back. We need to get the ID.
            r = connection.execute(
                device_series_migrator
                .select().where(
                    device_series_migrator.c.series_id == s_id,
                ).where(
                    device_series_migrator.c.device_id == d_id
                ))

            # cache the result for future iterations.
            seen_device_series[(s_id, d_id)] = dict(r.first())

        device_series = seen_device_series[(s_id, d_id)]

        # Update the data_point table to populate the new device_series_id.
        connection.execute(
            data_point_migrator.update().where(
                data_point_migrator.c.id == data_point.id
            ).values(
                device_series_id=device_series['id']
            )
        )

    # Ok, now its fully populated. Disable nulls on the col. If there are still
    # nulls we will get an error here, so its a good sanity check.
    op.alter_column('data_point', 'device_series_id', nullable=False)

    # Finally, drop the two original columns as per the end of the original
    # alembic code.
    op.drop_column('data_point', 'series_id')
    op.drop_column('data_point', 'device_id')


def downgrade():
    op.add_column(
        'data_point', sa.Column('device_id', sa.INTEGER(), nullable=True))
    op.add_column(
        'data_point', sa.Column('series_id', sa.INTEGER(), nullable=True))
    op.drop_column('data_point', 'device_series_id')
    op.drop_table('device_series')
