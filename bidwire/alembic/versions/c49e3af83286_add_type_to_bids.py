"""add type to bids

Revision ID: c49e3af83286
Revises: b73811be5f44
Create Date: 2017-04-15 17:06:23.290506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c49e3af83286'
down_revision = 'b73811be5f44'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bids', sa.Column('site', sa.Text, server_default='COMMBUYS'))


def downgrade():
    op.drop_column('bids', sa.Column('site', sa.Text, server_default='COMMBUYS'))
