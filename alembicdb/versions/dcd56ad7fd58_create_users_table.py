"""create users table

Revision ID: dcd56ad7fd58
Revises: 3b5dc48250c9
Create Date: 2022-05-12 21:58:29.152244

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dcd56ad7fd58'
down_revision = '3b5dc48250c9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=False), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('phone', sa.String(11), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('is_staff', sa.Boolean(), server_default='FALSE', nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
