from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import (
    Base,
    Alan,
    Sube,
    Brans,
    Ders,
    DersCizelgesi,
    DersDetay
)

# ==================================================
# VERİTABANI
# ==================================================

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
# ŞUBELER
# ==================================================

def subeleri_getir():

    session = Session()

    subeler = (
        session.query(Sube)
        .filter(Sube.aktif == True)
        .order_by(Sube.sinif, Sube.sube)
        .all()
    )

    session.close()

    return subeler


def sube_ekle(sinif, sube, alan_id, ogrenci_sayisi):

    session = Session()

    yeni = Sube(
        sinif=sinif,
        sube=sube,
        alan_id=alan_id,
        ogrenci_sayisi=ogrenci_sayisi,
        aktif=True
    )

    session.add(yeni)
    session.commit()
    session.close()


# ==================================================
# BRANŞLAR
# ==================================================

def branslari_getir():

    session = Session()

    branslar = (
        session.query(Brans)
        .filter(Brans.aktif == True)
        .order_by(Brans.brans_adi)
        .all()
    )

    session.close()

    return branslar


def brans_ekle(brans_adi):

    session = Session()

    brans = Brans(
        brans_adi=brans_adi,
        aktif=True
    )

    session.add(brans)
    session.commit()
    session.close()


# ==================================================
# DERSLER
# ==================================================

def dersleri_getir():

    session = Session()

    dersler = (
        session.query(Ders)
        .filter(Ders.aktif == True)
        .order_by(Ders.ders_adi)
        .all()
    )

    session.close()

    return dersler


def ders_ekle(ders_adi, kategori, brans_id=None, secmeli=False):

    session = Session()

    ders = Ders(
        ders_adi=ders_adi,
        kategori=kategori,
        brans_id=brans_id,
        secmeli=secmeli,
        aktif=True
    )

    session.add(ders)
    session.commit()
    session.close()


# ==================================================
# DERS ÇİZELGELERİ
# ==================================================

def cizelgeleri_getir():

    session = Session()

    liste = (
        session.query(DersCizelgesi)
        .filter(DersCizelgesi.aktif == True)
        .order_by(
            DersCizelgesi.yil.desc(),
            DersCizelgesi.adi
        )
        .all()
    )

    session.close()

    return liste


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


# ==================================================
# DERS ÇİZELGESİ DETAYLARI
# ==================================================

def cizelge_detayi_getir(cizelge_id):

    session = Session()

    detaylar = (
        session.query(DersDetay)
        .filter(DersDetay.cizelge_id == cizelge_id)
        .order_by(
            DersDetay.sinif,
            DersDetay.ders_id
        )
        .all()
    )

    session.close()

    return detaylar


def cizelge_detay_ekle(
        cizelge_id,
        ders_id,
        sinif,
        haftalik_saat,
        teorik=0,
        uygulama=0):

    session = Session()

    detay = DersDetay(
        cizelge_id=cizelge_id,
        ders_id=ders_id,
        sinif=sinif,
        haftalik_saat=haftalik_saat,
        teorik=teorik,
        uygulama=uygulama
    )

    session.add(detay)
    session.commit()
    session.close()

# ==================================================
# BRANŞLAR
# ==================================================

def branslari_getir():

    session = Session()

    branslar = (
        session.query(Brans)
        .filter(Brans.aktif == True)
        .order_by(Brans.brans_adi)
        .all()
    )

    session.close()

    return branslar


def brans_ekle(brans_adi):

    session = Session()

    yeni = Brans(
        brans_adi=brans_adi,
        aktif=True
    )

    session.add(yeni)
    session.commit()
    session.close()