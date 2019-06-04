from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

class TelegramUser(Base):
    __tablename__ = "telegram_users"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    active = Column(Boolean)

    def __init__(self, id, name, active):
        self.id = id
        self.name = name
        self.active = active

    def __repr__(self):
        return "%id=s,active=%s,name=%s" % (self.id, self.active, self.name)