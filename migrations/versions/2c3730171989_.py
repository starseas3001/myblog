"""empty message

Revision ID: 2c3730171989
Revises: a79c25504c80
Create Date: 2018-09-18 21:15:47.509806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c3730171989'
down_revision = 'a79c25504c80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('head_image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'head_image')
    # ### end Alembic commands ###
