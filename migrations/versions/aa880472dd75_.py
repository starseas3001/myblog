"""empty message

Revision ID: aa880472dd75
Revises: 8020d161821e
Create Date: 2018-09-20 14:43:13.876308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa880472dd75'
down_revision = '8020d161821e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('click_nums', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'click_nums')
    # ### end Alembic commands ###
