"""empty message

Revision ID: cca6483c4471
Revises: 
Create Date: 2018-09-11 23:08:30.951859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cca6483c4471'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('pwd', sa.String(length=100), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_admin_addtime'), 'admin', ['addtime'], unique=False)
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('contitle', sa.Text(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_article_add_time'), 'article', ['add_time'], unique=False)
    op.create_index(op.f('ix_article_title'), 'article', ['title'], unique=True)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nike_name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_add_time'), 'comment', ['add_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_add_time'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_article_title'), table_name='article')
    op.drop_index(op.f('ix_article_add_time'), table_name='article')
    op.drop_table('article')
    op.drop_index(op.f('ix_admin_addtime'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
