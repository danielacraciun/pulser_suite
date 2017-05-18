"""empty message

Revision ID: d84cb052d5e6
Revises: 4e9595d48fea
Create Date: 2017-05-14 22:01:42.165862

"""

# revision identifiers, used by Alembic.
revision = 'd84cb052d5e6'
down_revision = '4e9595d48fea'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hr_sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Text(), nullable=True),
    sa.Column('client_secret', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movement_sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secret_key', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('imu_key')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('imu_key',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('secret_key', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('movement_sensor')
    op.drop_table('hr_sensor')
    # ### end Alembic commands ###