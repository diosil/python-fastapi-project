"""phone_number

Revision ID: 194914509dce
Revises: 8b138666b6b1
Create Date: 2023-05-20 19:38:23.235222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194914509dce'
down_revision = '8b138666b6b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
