op.add_column('users',
                  sa.Column('balance', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'balance')