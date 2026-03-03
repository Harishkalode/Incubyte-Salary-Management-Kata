"""Initial migration: create employees table

Revision ID: bcb4d7d7f804
Revises: 
Create Date: 2026-03-03 05:31:17.270631

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcb4d7d7f804'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create employees table
    op.create_table('employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('job_title', sa.String(255), nullable=False),
        sa.Column('country', sa.String(100), nullable=False),
        sa.Column('salary', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')
