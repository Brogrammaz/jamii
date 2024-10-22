"""updated deposit table

Revision ID: eb022174497b
Revises: d7a756c09e27
Create Date: 2024-10-22 17:05:35.357158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb022174497b'
down_revision: Union[str, None] = 'd7a756c09e27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_unique_constraint('uq_tbl_users_user_id', 'tbl_users', ['user_id'])

    op.create_table('tbl_deposits',
    sa.Column('deposit_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['tbl_users.user_id'], ),
    sa.PrimaryKeyConstraint('deposit_id')
    )
    op.create_index(op.f('ix_tbl_deposits_deposit_id'), 'tbl_deposits', ['deposit_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_tbl_users_user_id', 'tbl_users', type_='unique')
    op.drop_index(op.f('ix_tbl_deposits_deposit_id'), table_name='tbl_deposits')
    op.drop_table('tbl_deposits')
    # ### end Alembic commands ###
