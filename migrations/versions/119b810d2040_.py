"""empty message

Revision ID: 119b810d2040
Revises: 30c2ff117f87
Create Date: 2020-12-29 17:25:21.034647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '119b810d2040'
down_revision = '30c2ff117f87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('picture_path', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('color', sa.String(length=10), nullable=True),
    sa.Column('size', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Product')
    # ### end Alembic commands ###