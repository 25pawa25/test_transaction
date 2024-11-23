"""add_amount_transaction

Revision ID: 27cc4096e9ca
Revises: 9df556f50576
Create Date: 2024-11-23 13:44:48.506763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27cc4096e9ca'
down_revision = '9df556f50576'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction_history', sa.Column('amount', sa.DECIMAL(precision=15, scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction_history', 'amount')
    # ### end Alembic commands ###
