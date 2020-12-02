from sqlalchemy import Column, String

from app.classes import Base


class Setting(Base):
    __tablename__ = 'settings'
    key = Column(String(200), primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<Setting('%s','%s')>" % (self.key, self.value)