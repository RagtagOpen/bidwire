"""create notices table

Revision ID: fbd6ae18c51c
Revises: 9b30b0fe231a
Create Date: 2017-06-08 20:11:48.397567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd6ae18c51c'
down_revision = '9b30b0fe231a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'notices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('description', sa.Text),
        sa.Column('title', sa.Text),
        sa.Column('href', sa.Text),
        sa.Column('start', sa.DateTime),
        sa.Column('end', sa.DateTime),
        sa.Column('posted', sa.DateTime),
        sa.Column('location', sa.Text),
        sa.Column('thoroughfare', sa.Text),
        sa.Column('premise', sa.Text),
        sa.Column('city', sa.Text),
        sa.Column('state', sa.Text),
        sa.Column('postcode', sa.Text),
        sa.Column('site', sa.Text)
    )


def downgrade():
    op.drop_table('notices')
