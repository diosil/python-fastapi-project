"""create posts tables

Revision ID: e33f94d40be6
Revises: 
Create Date: 2023-05-20 16:09:33.465855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e33f94d40be6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                            , sa.Column('title', sa.String(), nullable=True)
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
