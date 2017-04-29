"""create documents table

Revision ID: 9b30b0fe231a
Revises: 9a1ee025e55d
Create Date: 2017-04-26 01:54:20.304635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b30b0fe231a'
down_revision = '9a1ee025e55d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url', sa.String, unique=True),
        sa.Column('title', sa.String),
        sa.Column('site', sa.String),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )


def downgrade():
    op.drop_table('documents')
