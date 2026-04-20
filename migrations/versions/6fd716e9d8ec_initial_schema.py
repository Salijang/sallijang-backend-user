"""initial_schema

Revision ID: 6fd716e9d8ec
Revises:
Create Date: 2026-04-20 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '6fd716e9d8ec'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('buyer', 'seller', name='roleenum'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='user_schema',
    )
    op.create_index('ix_user_schema_users_id', 'users', ['id'], unique=False, schema='user_schema')
    op.create_index('ix_user_schema_users_email', 'users', ['email'], unique=True, schema='user_schema')

    op.create_table(
        'wishlists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user_schema.users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema='user_schema',
    )
    op.create_index('ix_user_schema_wishlists_id', 'wishlists', ['id'], unique=False, schema='user_schema')


def downgrade() -> None:
    op.drop_index('ix_user_schema_wishlists_id', table_name='wishlists', schema='user_schema')
    op.drop_table('wishlists', schema='user_schema')
    op.drop_index('ix_user_schema_users_email', table_name='users', schema='user_schema')
    op.drop_index('ix_user_schema_users_id', table_name='users', schema='user_schema')
    op.drop_table('users', schema='user_schema')
    op.execute('DROP TYPE IF EXISTS roleenum')
