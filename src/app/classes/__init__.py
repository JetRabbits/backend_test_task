from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

from app.classes.user_session import UserSession
from app.classes.setting import Setting