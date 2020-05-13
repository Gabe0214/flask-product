"""image-url column added to products 

Revision ID: dc8d5d1f9dda
Revises: 0a921221aace
Create Date: 2020-05-11 08:16:18.083328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc8d5d1f9dda'
down_revision = '0a921221aace'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'image_url')
    # ### end Alembic commands ###
