"""add foreign key to meals

Revision ID: cd178b819c63
Revises: a0e96c176669
Create Date: 2022-05-12 22:15:06.321696

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cd178b819c63'
down_revision = 'a0e96c176669'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('meals',
                  sa.Column('category_id', sa.Integer(), nullable=False))
    op.create_foreign_key('meals_category_id_fkey', source_table='meals', referent_table='categories',
                          local_cols=['category_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('meals_category_id_fkey', table_name='meals')
    op.drop_column('meals', 'category_id')
    pass
