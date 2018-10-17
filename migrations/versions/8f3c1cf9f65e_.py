"""empty message

Revision ID: 8f3c1cf9f65e
Revises: b9093b520181
Create Date: 2018-09-23 10:55:21.388495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3c1cf9f65e'
down_revision = 'b9093b520181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accesslog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accesslog_add_time'), 'accesslog', ['add_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accesslog_add_time'), table_name='accesslog')
    op.drop_table('accesslog')
    # ### end Alembic commands ###
