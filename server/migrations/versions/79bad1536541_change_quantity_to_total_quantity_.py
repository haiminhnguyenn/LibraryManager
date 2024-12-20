"""Change 'quantity' to 'total_quantity' & 'available_quantity' in 'books'

Revision ID: 79bad1536541
Revises: 435bc2494412
Create Date: 2024-12-13 11:41:06.727967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79bad1536541'
down_revision = '435bc2494412'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_quantity', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('available_quantity', sa.Integer(), nullable=False))
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('available_quantity')
        batch_op.drop_column('total_quantity')

    # ### end Alembic commands ###
