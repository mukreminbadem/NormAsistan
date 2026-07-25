from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import declarative_base, relationship

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
        default=datetime.now,
        nullable=False
    )

    guncelleme_tarihi = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
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
        index=True,
        nullable=False
    )

    subeler = relationship(
        "Sube",
        back_populates="alan"
    )

    def __repr__(self):
        return f"<Alan(id={self.id}, ad='{self.alan_adi}')>"


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
        ForeignKey("alanlar.id"),
        nullable=True
    )

    ogrenci_sayisi = Column(
        Integer,
        default=0,
        nullable=False
    )

    alan = relationship(
        "Alan",
        back_populates="subeler"
    )

    def __repr__(self):
        return f"<Sube({self.sinif}/{self.sube})>"


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
        index=True,
        nullable=True
    )

    brans_adi = Column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    dersler = relationship(
        "Ders",
        back_populates="brans"
    )

    def __repr__(self):
        return f"<Brans('{self.brans_adi}')>"


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
        index=True,
        nullable=False
    )

    kategori = Column(
        String(50),
        nullable=True
    )

    brans_id = Column(
        Integer,
        ForeignKey("branslar.id"),
        nullable=True
    )

    secmeli = Column(
        Boolean,
        default=False,
        nullable=False
    )

    brans = relationship(
        "Brans",
        back_populates="dersler"
    )

    detaylar = relationship(
        "DersDetay",
        back_populates="ders"
    )

    def __repr__(self):
        return f"<Ders('{self.ders_adi}')>"

# ==========================================================
# OKUL
# ==========================================================

class Okul(Base, OrtakAlanlar):

    __tablename__ = "okul"

    id = Column(
        Integer,
        primary_key=True
    )

    okul_adi = Column(
        String(200),
        nullable=False
    )

    egitim_yili = Column(
        String(20),
        nullable=False
    )

    okul_turu = Column(
        String(100),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<Okul(id={self.id}, okul_adi='{self.okul_adi}')>"
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

    detaylar = relationship(
        "DersDetay",
        back_populates="cizelge",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DersCizelgesi('{self.adi}')>"


# ==========================================================
# DERS ÇİZELGESİ DETAYLARI
# ==========================================================

class DersDetay(Base, OrtakAlanlar):

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
        default=0,
        nullable=False
    )

    teorik = Column(
        Integer,
        default=0,
        nullable=False
    )

    uygulama = Column(
        Integer,
        default=0,
        nullable=False
    )

    cizelge = relationship(
        "DersCizelgesi",
        back_populates="detaylar"
    )

    ders = relationship(
        "Ders",
        back_populates="detaylar"
    )

    def __repr__(self):
        return (
            f"<DersDetay("
            f"sinif={self.sinif}, "
            f"ders_id={self.ders_id}, "
            f"saat={self.haftalik_saat})>"
        )