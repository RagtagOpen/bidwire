"""empty message

Revision ID: d9ecfca6c414
Revises: a1b42c9006a7
Create Date: 2017-07-27 04:02:11.126675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9ecfca6c414'
down_revision = 'a1b42c9006a7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('documents') as batch:
        batch.add_column(sa.Column('description', sa.String))


def downgrade():
    with op.batch_alter_table('documents') as batch:
        batch.drop_column('description')