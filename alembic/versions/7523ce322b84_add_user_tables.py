"""add user tables

Revision ID: 7523ce322b84
Revises: 69049897e665
Create Date: 2023-05-20 16:51:19.186732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7523ce322b84'
down_revision = '69049897e665'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False)
                           , sa.Column('email', sa.String(), nullable=False)
                           , sa.Column('password', sa.String(), nullable=False)
                           , sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default= sa.text('now()'), nullable=False)
                           , sa.PrimaryKeyConstraint('id')
                           , sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
