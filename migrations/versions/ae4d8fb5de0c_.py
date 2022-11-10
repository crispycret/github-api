"""empty message

Revision ID: ae4d8fb5de0c
Revises: 
Create Date: 2022-11-09 20:06:13.307376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae4d8fb5de0c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('author', sa.String(length=128), nullable=False),
    sa.Column('html_url', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_repo')),
    sa.UniqueConstraint('html_url', name=op.f('uq_repo_html_url')),
    sa.UniqueConstraint('name', name=op.f('uq_repo_name'))
    )
    op.create_table('commit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('author', sa.String(length=128), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('repo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['repo_id'], ['repo.id'], name=op.f('fk_commit_repo_id_repo')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_commit'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commit')
    op.drop_table('repo')
    # ### end Alembic commands ###
