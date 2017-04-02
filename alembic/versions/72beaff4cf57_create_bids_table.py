"""create bids table

Revision ID: 72beaff4cf57
Revises: 
Create Date: 2017-04-02 05:08:23.429195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72beaff4cf57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bids',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('identifier', sa.String, unique=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )


def downgrade():
    op.drop_table('bids')
