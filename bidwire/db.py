from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import bidwire_settings

engine = create_engine(bidwire_settings.POSTGRES_ENDPOINT)
## A factory of DB session objects
Session = sessionmaker(bind=engine)
