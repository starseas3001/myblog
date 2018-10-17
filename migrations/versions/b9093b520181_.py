"""empty message

Revision ID: b9093b520181
Revises: 45272cd1d985
Create Date: 2018-09-21 22:57:35.931176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9093b520181'
down_revision = '45272cd1d985'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verifycode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('code', sa.String(length=20), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_verifycode_add_time'), 'verifycode', ['add_time'], unique=False)
    op.add_column('admin', sa.Column('email', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin', 'email')
    op.drop_index(op.f('ix_verifycode_add_time'), table_name='verifycode')
    op.drop_table('verifycode')
    # ### end Alembic commands ###
