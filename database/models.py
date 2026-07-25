from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Alan(Base):
    __tablename__ = "alanlar"

    id = Column(Integer, primary_key=True)
    alan_adi = Column(String, unique=True)
    aktif = Column(Boolean, default=True)