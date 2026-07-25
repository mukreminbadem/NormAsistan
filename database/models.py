from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Alan(Base):
    __tablename__ = "alanlar"

    id = Column(Integer, primary_key=True)
    alan_adi = Column(String, unique=True)
    aktif = Column(Boolean, default=True)


class DersCizelgesi(Base):
    __tablename__ = "ders_cizelgeleri"

    id = Column(Integer, primary_key=True)
    adi = Column(String)
    program = Column(String)
    yil = Column(String)
    aktif = Column(Boolean, default=True)


class Ders(Base):
    __tablename__ = "dersler"

    id = Column(Integer, primary_key=True)
    ders_adi = Column(String)
    kategori = Column(String)


class DersDetay(Base):
    __tablename__ = "ders_detaylari"

    id = Column(Integer, primary_key=True)

    cizelge_id = Column(
        Integer,
        ForeignKey("ders_cizelgeleri.id")
    )

    ders_id = Column(
        Integer,
        ForeignKey("dersler.id")
    )

    sinif = Column(Integer)

    haftalik_saat = Column(Integer)