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
    event_date = Column(DateTime)
    post_date = Column(DateTime)
    location = Column(Text)
    site = Column(Text, default=Site.BOSTON.name)

    def get_url(self):
        if self.site == Notice.Site.BOSTON.name:
            return "https://www.boston.gov/public-notices"
        raise NotImplementedError