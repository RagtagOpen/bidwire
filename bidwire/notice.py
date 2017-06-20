from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, func, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from enum import Enum

Base = declarative_base()


class Notice(Base):
    class Site(Enum):
        BOSTON = "Boston's Public Notices page"
    __tablename__ = 'notices'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    description = Column(Text)
    title = Column(Text)
    href = Column(Text)
    start = Column(DateTime)
    end = Column(DateTime)
    posted = Column(DateTime)
    fetched = Column(DateTime)
    location = Column(Text)
    thoroughfare = Column(Text)
    premise = Column(Text)
    city = Column(Text)
    state = Column(Text)
    postcode = Column(Text)
    site = Column(Text, default=Site.BOSTON.name)

    def get_url(self):
        if self.site == Notice.Site.BOSTON.name:
            return "https://www.boston.gov/public-notices"
        raise NotImplementedError