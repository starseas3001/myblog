"""empty message

Revision ID: 6624f08e9a63
Revises: 8287478757dc
Create Date: 2018-09-17 20:06:43.561322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6624f08e9a63'
down_revision = '8287478757dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'image')
    # ### end Alembic commands ###
