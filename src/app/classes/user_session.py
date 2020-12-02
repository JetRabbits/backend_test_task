from sqlalchemy import Column, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from app.classes import Base


class UserSession(Base):
    __tablename__ = 'sessions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    person_id = Column(UUID(as_uuid=True))
    role = Column(BigInteger)
    token = Column(String)
    ip = Column(String)
    created_when = Column(TIMESTAMP(timezone=True))
    mobile_version = Column(String)
    platform = Column(String)

    def __init__(self, id, person_id, role, token, ip, created_when, mobile_version, platform):
        self.id = id
        self.person_id = person_id
        self.role = role
        self.token = token
        self.ip = ip
        self.created_when = created_when
        self.mobile_version = mobile_version
        self.platform = platform

    def __repr__(self):
        return "<Session('%s','%s', '%s', '%s', '%s', '%s')>" % \
               (self.id, self.person_id, self.token, self.ip, self.mobile_version, self.platform)