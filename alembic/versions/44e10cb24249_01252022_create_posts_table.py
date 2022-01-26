"""01252022: Create posts table

Revision ID: 44e10cb24249
Revises: 
Create Date: 2022-01-25 20:06:45.317900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44e10cb24249'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    pass


def downgrade():
    op.drop_table('post')
    pass
