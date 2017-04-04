"""add all basic bid fields

Revision ID: b73811be5f44
Revises: 72beaff4cf57
Create Date: 2017-04-03 00:53:50.692376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b73811be5f44'
down_revision = '72beaff4cf57'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bids', sa.Column('description', sa.Text))
    op.add_column('bids', sa.Column('department', sa.Text))
    op.add_column('bids', sa.Column('organization', sa.Text))
    op.add_column('bids', sa.Column('location', sa.Text))
    op.add_column('bids', sa.Column('open_date', sa.DateTime))
    op.add_column('bids', sa.Column('items', sa.JSON))


def downgrade():
    op.drop_column('bids', sa.Column('description', sa.Text))
    op.drop_column('bids', sa.Column('department', sa.Text))
    op.drop_column('bids', sa.Column('organization', sa.Text))
    op.drop_column('bids', sa.Column('location', sa.Text))
    op.drop_column('bids', sa.Column('open_date', sa.DateTime))
    op.drop_column('bids', sa.Column('items', sa.JSON))
