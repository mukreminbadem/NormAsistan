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

def alanlari_getir(aktif=True):

    session = Session()

    try:

        sorgu = session.query(Alan)

        if aktif is not None:
            sorgu = sorgu.filter(Alan.aktif == aktif)

        return sorgu.order_by(Alan.alan_adi).all()

    finally:
        session.close()


def alan_ekle(alan_adi):

    session = Session()

    try:

        alan_adi = alan_adi.strip()

        kayit = (
            session.query(Alan)
            .filter(Alan.alan_adi == alan_adi)
            .first()
        )

        if kayit:

            if not kayit.aktif:
                kayit.aktif = True
                session.commit()

            return False

        yeni = Alan(
            alan_adi=alan_adi,
            aktif=True
        )

        session.add(yeni)
        session.commit()

        return True

    finally:
        session.close()


def alan_sil(alan_id):

    session = Session()

    try:

        alan = session.get(Alan, alan_id)

        if alan:
            alan.aktif = False
            session.commit()

    finally:
        session.close()


# ==================================================
# ŞUBELER
# ==================================================

def subeleri_getir():

    session = Session()

    try:

        return (
            session.query(Sube)
            .filter(Sube.aktif == True)
            .order_by(Sube.sinif, Sube.sube)
            .all()
        )

    finally:
        session.close()


def sube_ekle(sinif, sube, alan_id, ogrenci_sayisi):

    session = Session()

    try:

        yeni = Sube(
            sinif=sinif,
            sube=sube,
            alan_id=alan_id,
            ogrenci_sayisi=ogrenci_sayisi,
            aktif=True
        )

        session.add(yeni)
        session.commit()

    finally:
        session.close()


# ==================================================
# BRANŞLAR
# ==================================================

def branslari_getir(aktif=True):

    session = Session()

    try:

        sorgu = session.query(Brans)

        if aktif is not None:
            sorgu = sorgu.filter(Brans.aktif == aktif)

        return sorgu.order_by(Brans.brans_adi).all()

    finally:
        session.close()


def brans_ekle(brans_adi, meb_kodu=""):

    session = Session()

    try:

        brans_adi = brans_adi.strip()
        meb_kodu = meb_kodu.strip()

        kayit = (
            session.query(Brans)
            .filter(Brans.brans_adi == brans_adi)
            .first()
        )

        if kayit:

            if not kayit.aktif:

                kayit.aktif = True
                kayit.meb_kodu = meb_kodu

                session.commit()

            return False

        yeni = Brans(
            brans_adi=brans_adi,
            meb_kodu=meb_kodu,
            aktif=True
        )

        session.add(yeni)
        session.commit()

        return True

    finally:
        session.close()


def brans_guncelle(brans_id, brans_adi, meb_kodu):

    session = Session()

    try:

        brans = session.get(Brans, brans_id)

        if brans:

            brans.brans_adi = brans_adi.strip()
            brans.meb_kodu = meb_kodu.strip()

            session.commit()

            return True

        return False

    finally:
        session.close()


def brans_sil(brans_id):

    session = Session()

    try:

        brans = session.get(Brans, brans_id)

        if brans:

            brans.aktif = False
            session.commit()

    finally:
        session.close()


# ==================================================
# DERSLER
# ==================================================

def dersleri_getir():

    session = Session()

    try:

        return (
            session.query(Ders)
            .filter(Ders.aktif == True)
            .order_by(Ders.ders_adi)
            .all()
        )

    finally:
        session.close()


def ders_ekle(ders_adi,
               kategori,
               brans_id=None,
               secmeli=False):

    session = Session()

    try:

        ders = Ders(
            ders_adi=ders_adi,
            kategori=kategori,
            brans_id=brans_id,
            secmeli=secmeli,
            aktif=True
        )

        session.add(ders)
        session.commit()

    finally:
        session.close()


# ==================================================
# DERS ÇİZELGELERİ
# ==================================================

def cizelgeleri_getir():

    session = Session()

    try:

        return (
            session.query(DersCizelgesi)
            .filter(DersCizelgesi.aktif == True)
            .order_by(
                DersCizelgesi.yil.desc(),
                DersCizelgesi.adi
            )
            .all()
        )

    finally:
        session.close()


def cizelge_ekle(adi, program, yil):

    session = Session()

    try:

        yeni = DersCizelgesi(
            adi=adi,
            program=program,
            yil=yil,
            aktif=True
        )

        session.add(yeni)
        session.commit()

    finally:
        session.close()


# ==================================================
# DERS ÇİZELGESİ DETAYLARI
# ==================================================

def cizelge_detayi_getir(cizelge_id):

    session = Session()

    try:

        return (
            session.query(DersDetay)
            .filter(DersDetay.cizelge_id == cizelge_id)
            .order_by(
                DersDetay.sinif,
                DersDetay.ders_id
            )
            .all()
        )

    finally:
        session.close()


def cizelge_detay_ekle(
        cizelge_id,
        ders_id,
        sinif,
        haftalik_saat,
        teorik=0,
        uygulama=0):

    session = Session()

    try:

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

    finally:
        session.close()