"""absolute_massgov_eopss_url

Revision ID: a1b42c9006a7
Revises: 9b30b0fe231a
Create Date: 2017-06-26 00:02:45.998655

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from document import Document
from urllib import parse

# revision identifiers, used by Alembic.
revision = 'a1b42c9006a7'
down_revision = '9b30b0fe231a'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # This migration was a one-time fix of data, and doesn't need to be run ever
    # again, and gets in the way of future modifications to the Document class.
    # It's left here for version number continuity, but is otherwise dead.
#    def ensure_absolute(url):
#        root_url = "https://www.mass.gov/"
#        if not url.startswith(root_url):
#            return parse.urljoin(root_url, url)
#        return url
#
#    # Attach to the migration's session
#    session = Session(bind=op.get_bind())
#    docs = session.query(Document).filter(
#        Document.site == Document.Site.MASSGOV_EOPSS.name).all()
#    for doc in docs:
#        doc.url = ensure_absolute(doc.url)
#    session.add_all(docs)
#    session.commit()


def downgrade():
    # Do nothing for the rollback.
    pass
