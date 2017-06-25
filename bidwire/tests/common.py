import db
from sqlalchemy import orm

# A test-only scoped ORM session.
Session = orm.scoped_session(orm.sessionmaker())
Session.configure(bind=db.engine)
