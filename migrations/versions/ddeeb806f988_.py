"""empty message

Revision ID: ddeeb806f988
Revises: a8c680c9354e
Create Date: 2021-01-02 00:54:17.225977

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ddeeb806f988'
down_revision = 'a8c680c9354e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('postcode', sa.String(length=20), nullable=True))
    op.drop_column('address', 'telephone')
    op.drop_column('address', 'fax')
    op.add_column('profile', sa.Column('fax', sa.String(length=30), nullable=True))
    op.add_column('profile', sa.Column('telephone', sa.String(length=20), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profile', 'telephone')
    op.drop_column('profile', 'fax')
    op.add_column('address', sa.Column('fax', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('address', sa.Column('telephone', mysql.VARCHAR(length=20), nullable=False))
    op.drop_column('address', 'postcode')
    # ### end Alembic commands ###
