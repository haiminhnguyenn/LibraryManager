"""Add new column 'quantity' into table 'books'

Revision ID: dc37fb261e87
Revises: bd2b7daf5948
Create Date: 2024-11-23 21:52:26.036430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc37fb261e87'
down_revision = 'bd2b7daf5948'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###