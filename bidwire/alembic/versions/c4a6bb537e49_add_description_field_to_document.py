"""Add description field to Document

Revision ID: c4a6bb537e49
Revises: fbd6ae18c51c
Create Date: 2017-06-21 19:02:09.414328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a6bb537e49'
down_revision = '9b30b0fe231a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('documents') as batch:
        batch.add_column(sa.Column('description', sa.String))


def downgrade():
    with op.batch_alter_table('documents') as batch:
        batch.drop_column('description')
