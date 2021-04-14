"""create Category model

Revision ID: 31d6f8450eb5
Revises: fe2bea594bc0
Create Date: 2021-04-14 16:34:58.070745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31d6f8450eb5'
down_revision = 'fe2bea594bc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    # ### end Alembic commands ###