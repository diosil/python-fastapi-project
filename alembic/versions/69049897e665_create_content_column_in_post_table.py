"""create content column in post table

Revision ID: 69049897e665
Revises: e33f94d40be6
Create Date: 2023-05-20 16:45:42.057439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69049897e665'
down_revision = 'e33f94d40be6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
