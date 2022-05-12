"""create categories table

Revision ID: a0e96c176669
Revises: dcd56ad7fd58
Create Date: 2022-05-12 22:12:08.424049

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a0e96c176669'
down_revision = 'dcd56ad7fd58'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('categories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('slug', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    pass


def downgrade():
    op.drop_table('categories')
    pass
