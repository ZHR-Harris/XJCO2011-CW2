"""empty message

Revision ID: 53feed15303d
Revises: 78848e40513a
Create Date: 2021-01-02 16:00:02.198402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53feed15303d'
down_revision = '78848e40513a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('product_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'review', 'Product', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'review', type_='foreignkey')
    op.drop_column('review', 'product_id')
    # ### end Alembic commands ###
