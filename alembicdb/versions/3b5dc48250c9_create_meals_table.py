"""create meals table

Revision ID: 3b5dc48250c9
Revises: 
Create Date: 2022-05-12 21:43:18.798506

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3b5dc48250c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('meals',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('slug', sa.String(), nullable=False),
                    sa.Column('price', sa.Integer, nullable=False),
                    sa.Column('protein', sa.Integer, server_default='0', nullable=False),
                    sa.Column('fats', sa.Integer, server_default='0', nullable=False),
                    sa.Column('carbs', sa.Integer, server_default='0', nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('available_inventory', sa.Integer(), server_default='0', nullable=False))
    pass


def downgrade():
    op.drop_table('meals')
    pass
