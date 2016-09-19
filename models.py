import os

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'app.db'))
Base = declarative_base()
DBSession = sessionmaker(bind=engine)


def get_database_session():
    return DBSession()


class FitbitInfo(Base):
    __tablename__ = 'fitbit-info'
    fitbit_id = Column(String(50), primary_key=True)
    refresh_token = Column(String(120))
    access_token = Column(String(120))

    def __init__(self, fitbit_id, refresh_token, access_token):
        self.fitbit_id = fitbit_id
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __repr__(self):
        return '<Token %s>' % self.fitbit_id

    def __str__(self):
        return self.fitbit_id


Base.metadata.create_all(engine)

