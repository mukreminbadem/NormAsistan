from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


# ==================================================
# ALANLAR
# ==================================================

class Alan(Base):
    __tablename__ = "alanlar"

    id = Column(Integer, primary_key=True)

    alan_adi = Column(
        String,
        unique=True,
        nullable=False
    )

    aktif = Column(
        Boolean,
        default=True
    )


# ==================================================
# ŞUBELER
# ==================================================

class Sube(Base):
    __tablename__ = "subeler"

    id = Column(Integer, primary_key=True)

    sinif = Column(Integer)

    sube = Column(String)

    alan_id = Column(
        Integer,
        ForeignKey("alanlar.id")
    )

    ogrenci_sayisi = Column(Integer)

    aktif = Column(
        Boolean,
        default=True
    )


# ==================================================
# BRANŞLAR
# ==================================================

class Brans(Base):
    __tablename__ = "branslar"

    id = Column(Integer, primary_key=True)

    brans_adi = Column(
        String,
        unique=True,
        nullable=False
    )

    aktif = Column(
        Boolean,
        default=True
    )


# ==================================================
# DERSLER
# ==================================================

class Ders(Base):
    __tablename__ = "dersler"

    id = Column(Integer, primary_key=True)

    ders_adi = Column(
        String,
        nullable=False
    )

    kategori = Column(String)

    brans_id = Column(
        Integer,
        ForeignKey("branslar.id"),
        nullable=True
    )

    secmeli = Column(
        Boolean,
        default=False
    )

    aktif = Column(
        Boolean,
        default=True
    )


# ==================================================
# DERS ÇİZELGELERİ
# ==================================================

class DersCizelgesi(Base):
    __tablename__ = "ders_cizelgeleri"

    id = Column(Integer, primary_key=True)

    adi = Column(String)

    program = Column(String)

    yil = Column(String)

    aktif = Column(
        Boolean,
        default=True
    )


# ==================================================
# DERS ÇİZELGESİ DETAYI
# ==================================================

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

    teorik = Column(
        Integer,
        default=0
    )

    uygulama = Column(
        Integer,
        default=0
    )