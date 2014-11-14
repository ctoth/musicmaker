from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
engine = create_engine('postgresql://lyrics:lyrics1@allinaccess.com')

class Updater(object):

	def update(self, dct):
		for item, value in dct.iteritems():
			if not hasattr(self, item):
				raise KeyError("Item %s not found in model %s" % (item, self))
			if isinstance(value, dict):
				getattr(self, item).update(value)
			elif getattr(self, item) is None:
				setattr(self, item, value)

Base = declarative_base(cls=Updater)
Base.metadata.reflect(engine)
metadata = Base.metadata

class Artist(Base):
	__table__ = metadata.tables['artists']

class Song(Base):
	__table__ = metadata.tables['songs']
	artist = relationship('Artist', backref='songs', lazy='joined')

session = scoped_session(sessionmaker(engine))
