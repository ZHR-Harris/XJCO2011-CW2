"""empty message

Revision ID: 03a4a533e148
Revises: 9d74cc6335a4
Create Date: 2021-01-02 01:49:10.267048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03a4a533e148'
down_revision = '9d74cc6335a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('address_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('province', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.Column('postcode', sa.String(length=20), nullable=True),
    sa.Column('default_address', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('address_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('address')
    # ### end Alembic commands ###
