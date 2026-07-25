from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


# ==========================================================
# ORTAK ALANLAR
# ==========================================================

class OrtakAlanlar:

    aktif = Column(
        Boolean,
        default=True,
        nullable=False
    )

    olusturma_tarihi = Column(
        DateTime,
        default=datetime.now
    )

    guncelleme_tarihi = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )


# ==========================================================
# ALANLAR
# ==========================================================

class Alan(Base, OrtakAlanlar):

    __tablename__ = "alanlar"

    id = Column(
        Integer,
        primary_key=True
    )

    alan_adi = Column(
        String(100),
        unique=True,
        nullable=False
    )


# ==========================================================
# ŞUBELER
# ==========================================================

class Sube(Base, OrtakAlanlar):

    __tablename__ = "subeler"

    id = Column(
        Integer,
        primary_key=True
    )

    sinif = Column(
        Integer,
        nullable=False
    )

    sube = Column(
        String(5),
        nullable=False
    )

    alan_id = Column(
        Integer,
        ForeignKey("alanlar.id")
    )

    ogrenci_sayisi = Column(
        Integer,
        default=0
    )


# ==========================================================
# BRANŞLAR
# ==========================================================

class Brans(Base, OrtakAlanlar):

    __tablename__ = "branslar"

    id = Column(
        Integer,
        primary_key=True
    )

    meb_kodu = Column(
        String(20),
        unique=True,
        nullable=True
    )

    brans_adi = Column(
        String(150),
        unique=True,
        nullable=False
    )


# ==========================================================
# DERSLER
# ==========================================================

class Ders(Base, OrtakAlanlar):

    __tablename__ = "dersler"

    id = Column(
        Integer,
        primary_key=True
    )

    ders_adi = Column(
        String(150),
        nullable=False
    )

    kategori = Column(
        String(50)
    )

    brans_id = Column(
        Integer,
        ForeignKey("branslar.id"),
        nullable=True
    )

    secmeli = Column(
        Boolean,
        default=False
    )


# ==========================================================
# DERS ÇİZELGELERİ
# ==========================================================

class DersCizelgesi(Base, OrtakAlanlar):

    __tablename__ = "ders_cizelgeleri"

    id = Column(
        Integer,
        primary_key=True
    )

    adi = Column(
        String(150),
        nullable=False
    )

    program = Column(
        String(100),
        nullable=False
    )

    yil = Column(
        String(20),
        nullable=False
    )


# ==========================================================
# DERS ÇİZELGESİ DETAYLARI
# ==========================================================

class DersDetay(Base):

    __tablename__ = "ders_detaylari"

    id = Column(
        Integer,
        primary_key=True
    )

    cizelge_id = Column(
        Integer,
        ForeignKey("ders_cizelgeleri.id"),
        nullable=False
    )

    ders_id = Column(
        Integer,
        ForeignKey("dersler.id"),
        nullable=False
    )

    sinif = Column(
        Integer,
        nullable=False
    )

    haftalik_saat = Column(
        Integer,
        default=0
    )

    teorik = Column(
        Integer,
        default=0
    )

    uygulama = Column(
        Integer,
        default=0
    )