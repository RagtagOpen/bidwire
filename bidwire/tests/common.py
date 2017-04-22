from sqlalchemy import orm

# A test-only scoped ORM session.
Session = orm.scoped_session(orm.sessionmaker())
