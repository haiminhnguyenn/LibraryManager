"""Initial migration

Revision ID: 68daa55cca2e
Revises: 
Create Date: 2024-11-23 14:14:30.537916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68daa55cca2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tokens',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('confirm_token', sa.String(), nullable=True),
    sa.Column('reset_token', sa.String(), nullable=True),
    sa.Column('verification_code', sa.String(length=6), nullable=True),
    sa.Column('reset_code', sa.String(length=6), nullable=True),
    sa.Column('verification_code_expiration', sa.DateTime(), nullable=True),
    sa.Column('reset_code_expiration', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    op.drop_table('users')
    # ### end Alembic commands ###
