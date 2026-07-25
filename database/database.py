from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import (
    Base,
    Alan,
    Ders,
    DersCizelgesi
)

# -------------------------------
# Veritabanı Bağlantısı
# -------------------------------

engine = create_engine(
    "sqlite:///data/normasistan.db",
    echo=False
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# ==================================================
# ALANLAR
# ==================================================

def alanlari_getir():

    session = Session()

    alanlar = (
        session.query(Alan)
        .filter(Alan.aktif == True)
        .order_by(Alan.alan_adi)
        .all()
    )

    session.close()

    return alanlar


def alan_ekle(alan_adi):

    session = Session()

    alan = Alan(
        alan_adi=alan_adi,
        aktif=True
    )

    session.add(alan)
    session.commit()
    session.close()


# ==================================================
# DERSLER
# ==================================================

def dersleri_getir():

    session = Session()

    dersler = (
        session.query(Ders)
        .order_by(Ders.ders_adi)
        .all()
    )

    session.close()

    return dersler


def ders_ekle(ders_adi, kategori):

    session = Session()

    ders = Ders(
        ders_adi=ders_adi,
        kategori=kategori
    )

    session.add(ders)
    session.commit()
    session.close()


# ==================================================
# DERS ÇİZELGELERİ
# ==================================================

def cizelgeleri_getir():

    session = Session()

    cizelgeler = (
        session.query(DersCizelgesi)
        .filter(DersCizelgesi.aktif == True)
        .order_by(DersCizelgesi.yil.desc())
        .all()
    )

    session.close()

    return cizelgeler


def cizelge_ekle(adi, program, yil):

    session = Session()

    cizelge = DersCizelgesi(
        adi=adi,
        program=program,
        yil=yil,
        aktif=True
    )

    session.add(cizelge)
    session.commit()
    session.close()