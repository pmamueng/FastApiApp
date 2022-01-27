"""01262022: Add user_id column to post with foreign key from user.id

Revision ID: b1813e14cddc
Revises: cc86ddd590c6
Create Date: 2022-01-26 21:07:57.357070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1813e14cddc'
down_revision = 'cc86ddd590c6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', 
                          referent_table='users', local_cols=['user_id'], 
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','user_id')
    pass
