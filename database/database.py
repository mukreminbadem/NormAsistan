from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from database.models import (
    Base,
    Okul,
    Alan,
    Sube,
    Brans,
    Ders,
    DersCizelgesi,
    DersDetay
)

# ==========================================================
# VERİTABANI
# ==========================================================

from pathlib import Path

Path("data").mkdir(parents=True, exist_ok=True)
Path("backup").mkdir(parents=True, exist_ok=True)

DATABASE_URL = "sqlite:///data/normasistan.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


def veritabani_olustur():
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)


# ==========================================================
# OTURUM YÖNETİMİ
# ==========================================================

class DatabaseSession:

    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):

        try:

            if exc_type is None:
                self.session.commit()

            else:
                self.session.rollback()

        finally:
            self.session.close()


# ==========================================================
# ORTAK CRUD
# ==========================================================

def kayit_getir(model, kayit_id):

    with DatabaseSession() as session:
        return session.get(model, kayit_id)


def kayit_sil(model, kayit_id):

    with DatabaseSession() as session:

        kayit = session.get(model, kayit_id)

        if kayit is None:
            return False

        if hasattr(kayit, "aktif"):
            kayit.aktif = False
        else:
            session.delete(kayit)

        return True

# ==========================================================
# OKUL
# ==========================================================

def okul_getir():

    with DatabaseSession() as session:

        return session.query(Okul).first()


def okul_kaydet(
        okul_adi,
        egitim_yili,
        okul_turu):

    with DatabaseSession() as session:

        okul = session.query(Okul).first()

        if okul is None:

            okul = Okul(
                okul_adi=okul_adi,
                egitim_yili=egitim_yili,
                okul_turu=okul_turu
            )

            session.add(okul)

        else:

            okul.okul_adi = okul_adi
            okul.egitim_yili = egitim_yili
            okul.okul_turu = okul_turu

        return True

# ==========================================================
# ALANLAR
# ==========================================================

def alanlari_getir(aktif=True):

    with DatabaseSession() as session:

        sorgu = session.query(Alan)

        if aktif is not None:
            sorgu = sorgu.filter(
                Alan.aktif == aktif
            )

        return sorgu.order_by(
            Alan.alan_adi
        ).all()


def alan_getir(alan_id):

    return kayit_getir(
        Alan,
        alan_id
    )


def alan_ekle(alan_adi):

    alan_adi = alan_adi.strip()

    with DatabaseSession() as session:

        mevcut = (
            session.query(Alan)
            .filter(
                Alan.alan_adi == alan_adi
            )
            .first()
        )

        if mevcut:

            if not mevcut.aktif:
                mevcut.aktif = True

            return False

        session.add(

            Alan(
                alan_adi=alan_adi,
                aktif=True
            )

        )

        return True


def alan_guncelle(
        alan_id,
        yeni_ad):

    with DatabaseSession() as session:

        alan = session.get(
            Alan,
            alan_id
        )

        if alan is None:
            return False

        alan.alan_adi = yeni_ad.strip()

        return True


def alan_pasif_yap(alan_id):

    return kayit_sil(
        Alan,
        alan_id
    )


# ==========================================================
# ŞUBELER
# ==========================================================

def subeleri_getir():

    with DatabaseSession() as session:

        return (

            session.query(Sube)
            .filter(
                Sube.aktif == True
            )
            .order_by(
                Sube.id.asc()
            )
            .all()

        )


def sube_getir(sube_id):

    return kayit_getir(
        Sube,
        sube_id
    )


def sube_ekle(
        sinif,
        sube,
        alan_id,
        ogrenci_sayisi):

    with DatabaseSession() as session:

        session.add(

            Sube(
                sinif=sinif,
                sube=sube,
                alan_id=alan_id,
                ogrenci_sayisi=ogrenci_sayisi,
                aktif=True
            )

        )

        return True
# ==========================================================
# ŞUBE GÜNCELLE
# ==========================================================

def sube_guncelle(
    sube_id,
    sinif,
    sube,
    alan_id,
    ogrenci_sayisi
):

    with DatabaseSession() as session:

        kayit = session.get(Sube, sube_id)

        if kayit is None:
            return False

        kayit.sinif = sinif
        kayit.sube = sube
        kayit.alan_id = alan_id
        kayit.ogrenci_sayisi = ogrenci_sayisi

        return True
# ==========================================================
# ŞUBE SİL
# ==========================================================

def sube_sil(sube_id):

    with DatabaseSession() as session:

        kayit = session.get(Sube, sube_id)

        if kayit is None:
            return False

        session.delete(kayit)

        return True
# ==========================================================
# BRANŞLAR
# ==========================================================

def branslari_getir(aktif=True):

    with DatabaseSession() as session:

        sorgu = session.query(Brans)

        if aktif is not None:
            sorgu = sorgu.filter(
                Brans.aktif == aktif
            )

        return (
            sorgu.order_by(
                Brans.id.asc()
            )
            .all()
        )


def brans_getir(brans_id):

    return kayit_getir(
        Brans,
        brans_id
    )


def brans_ekle(
        brans_adi,
        meb_kodu=""):

    brans_adi = brans_adi.strip()
    meb_kodu = meb_kodu.strip()

    with DatabaseSession() as session:

        mevcut = (
            session.query(Brans)
            .filter(
                Brans.brans_adi == brans_adi
            )
            .first()
        )

        if mevcut:

            if not mevcut.aktif:

                mevcut.aktif = True
                mevcut.meb_kodu = meb_kodu

            return False

        session.add(

            Brans(
                brans_adi=brans_adi,
                meb_kodu=meb_kodu,
                aktif=True
            )

        )

        return True


def brans_guncelle(
        brans_id,
        brans_adi,
        meb_kodu):

    with DatabaseSession() as session:

        brans = session.get(
            Brans,
            brans_id
        )

        if brans is None:
            return False

        brans.brans_adi = brans_adi.strip()
        brans.meb_kodu = meb_kodu.strip()

        return True


def brans_pasif_yap(brans_id):

    return kayit_sil(
        Brans,
        brans_id
    )


# ==========================================================
# DERSLER
# ==========================================================

def dersleri_getir(aktif=True):

    with DatabaseSession() as session:

        sorgu = session.query(Ders)

        if aktif is not None:
            sorgu = sorgu.filter(
                Ders.aktif == aktif
            )

        return (
            sorgu.order_by(
                Ders.id.asc()
            )
            .all()
        )


def ders_getir(ders_id):

    return kayit_getir(
        Ders,
        ders_id
    )


def ders_ekle(
        ders_adi,
        kategori,
        brans_id=None,
        secmeli=False):

    with DatabaseSession() as session:

        session.add(

            Ders(
                ders_adi=ders_adi.strip(),
                kategori=kategori,
                brans_id=brans_id,
                secmeli=secmeli,
                aktif=True
            )

        )

        return True


def ders_guncelle(
        ders_id,
        ders_adi,
        kategori,
        brans_id,
        secmeli):

    with DatabaseSession() as session:

        ders = session.get(
            Ders,
            ders_id
        )

        if ders is None:
            return False

        ders.ders_adi = ders_adi.strip()
        ders.kategori = kategori
        ders.brans_id = brans_id
        ders.secmeli = secmeli

        return True


def ders_pasif_yap(ders_id):

    return kayit_sil(
        Ders,
        ders_id
    )


# ==========================================================
# DERS ÇİZELGELERİ
# ==========================================================

def cizelgeleri_getir(aktif=True):

    with DatabaseSession() as session:

        sorgu = session.query(
            DersCizelgesi
        )

        if aktif is not None:

            sorgu = sorgu.filter(
                DersCizelgesi.aktif == aktif
            )

        return (

            sorgu.order_by(
                DersCizelgesi.yil.desc(),
                DersCizelgesi.adi
            ).all()

        )


def cizelge_getir(cizelge_id):

    return kayit_getir(
        DersCizelgesi,
        cizelge_id
    )


def cizelge_ekle(
        adi,
        program,
        yil):

    with DatabaseSession() as session:

        session.add(

            DersCizelgesi(
                adi=adi.strip(),
                program=program,
                yil=yil,
                aktif=True
            )

        )

        return True


def cizelge_guncelle(
        cizelge_id,
        adi,
        program,
        yil):

    with DatabaseSession() as session:

        cizelge = session.get(
            DersCizelgesi,
            cizelge_id
        )

        if cizelge is None:
            return False

        cizelge.adi = adi.strip()
        cizelge.program = program
        cizelge.yil = yil

        return True


def cizelge_pasif_yap(cizelge_id):

    return kayit_sil(
        DersCizelgesi,
        cizelge_id
    )
	
# ==========================================================
# DERS ÇİZELGESİ DETAYLARI
# ==========================================================

def cizelge_detayi_getir(cizelge_id):

    with DatabaseSession() as session:

        return (
            session.query(DersDetay)
            .filter(
                DersDetay.cizelge_id == cizelge_id
            )
            .order_by(
                DersDetay.sinif,
                DersDetay.ders_id
            )
            .all()
        )


def sinifa_gore_detaylar(cizelge_id, sinif):

    with DatabaseSession() as session:

        return (
            session.query(DersDetay)
            .filter(
                DersDetay.cizelge_id == cizelge_id,
                DersDetay.sinif == sinif
            )
            .order_by(
                DersDetay.ders_id
            )
            .all()
        )


def derse_gore_detaylar(ders_id):

    with DatabaseSession() as session:

        return (
            session.query(DersDetay)
            .filter(
                DersDetay.ders_id == ders_id
            )
            .all()
        )


def cizelge_detay_ekle(
        cizelge_id,
        ders_id,
        sinif,
        haftalik_saat,
        teorik=0,
        uygulama=0):

    with DatabaseSession() as session:

        session.add(

            DersDetay(
                cizelge_id=cizelge_id,
                ders_id=ders_id,
                sinif=sinif,
                haftalik_saat=haftalik_saat,
                teorik=teorik,
                uygulama=uygulama
            )

        )

        return True


def cizelge_detay_guncelle(
        detay_id,
        haftalik_saat,
        teorik,
        uygulama):

    with DatabaseSession() as session:

        detay = session.get(
            DersDetay,
            detay_id
        )

        if detay is None:
            return False

        detay.haftalik_saat = haftalik_saat
        detay.teorik = teorik
        detay.uygulama = uygulama

        return True


def cizelge_detay_sil(detay_id):

    with DatabaseSession() as session:

        detay = session.get(
            DersDetay,
            detay_id
        )

        if detay is None:
            return False

        session.delete(detay)

        return True


def cizelge_detaylarini_temizle(cizelge_id):

    with DatabaseSession() as session:

        (
            session.query(DersDetay)
            .filter(
                DersDetay.cizelge_id == cizelge_id
            )
            .delete()
        )

        return True


# ==========================================================
# İSTATİSTİKLER
# ==========================================================

def toplam_alan():

    with DatabaseSession() as session:

        return (
            session.query(Alan)
            .filter(Alan.aktif == True)
            .count()
        )


def toplam_sube():

    with DatabaseSession() as session:

        return (
            session.query(Sube)
            .filter(Sube.aktif == True)
            .count()
        )


def toplam_brans():

    with DatabaseSession() as session:

        return (
            session.query(Brans)
            .filter(Brans.aktif == True)
            .count()
        )


def toplam_ders():

    with DatabaseSession() as session:

        return (
            session.query(Ders)
            .filter(Ders.aktif == True)
            .count()
        )


def toplam_cizelge():

    with DatabaseSession() as session:

        return (
            session.query(DersCizelgesi)
            .filter(DersCizelgesi.aktif == True)
            .count()
        )


# ==========================================================
# YARDIMCI FONKSİYONLAR
# ==========================================================

def commit_or_rollback(session):

    try:

        session.commit()
        return True

    except SQLAlchemyError:

        session.rollback()
        raise


def yeni_oturum():

    return SessionLocal()


def veritabani_baglantisi():

    return engine
	
# ==========================================================
# ARAMA FONKSİYONLARI
# ==========================================================

def alan_ara(aranan):

    with DatabaseSession() as session:

        return (
            session.query(Alan)
            .filter(
                Alan.alan_adi.ilike(f"%{aranan}%"),
                Alan.aktif == True
            )
            .order_by(Alan.alan_adi)
            .all()
        )


def brans_ara(aranan):

    with DatabaseSession() as session:

        return (
            session.query(Brans)
            .filter(
                Brans.brans_adi.ilike(f"%{aranan}%"),
                Brans.aktif == True
            )
            .order_by(Brans.brans_adi)
            .all()
        )


def ders_ara(aranan):

    with DatabaseSession() as session:

        return (
            session.query(Ders)
            .filter(
                Ders.ders_adi.ilike(f"%{aranan}%"),
                Ders.aktif == True
            )
            .order_by(Ders.ders_adi)
            .all()
        )


# ==========================================================
# KONTROL FONKSİYONLARI
# ==========================================================

def alan_kullaniliyor_mu(alan_id):

    with DatabaseSession() as session:

        return (
            session.query(Sube)
            .filter(
                Sube.alan_id == alan_id,
                Sube.aktif == True
            )
            .count()
        ) > 0


def brans_kullaniliyor_mu(brans_id):

    with DatabaseSession() as session:

        return (
            session.query(Ders)
            .filter(
                Ders.brans_id == brans_id,
                Ders.aktif == True
            )
            .count()
        ) > 0


def ders_kullaniliyor_mu(ders_id):

    with DatabaseSession() as session:

        return (
            session.query(DersDetay)
            .filter(
                DersDetay.ders_id == ders_id
            )
            .count()
        ) > 0


# ==========================================================
# TOPLU EKLEME
# ==========================================================

def alanlari_toplu_ekle(veriler):

    with DatabaseSession() as session:

        for alan in veriler:

            session.add(
                Alan(
                    alan_adi=alan,
                    aktif=True
                )
            )

        return True


def branslari_toplu_ekle(veriler):

    with DatabaseSession() as session:

        for ad, kod in veriler:

            session.add(
                Brans(
                    brans_adi=ad,
                    meb_kodu=kod,
                    aktif=True
                )
            )

        return True


# ==========================================================
# NORM HESAPLAMA SORGULARI
# ==========================================================

def bransa_gore_toplam_saat(brans_id):

    with DatabaseSession() as session:

        sonuc = (
            session.query(DersDetay)
            .join(Ders)
            .filter(
                Ders.brans_id == brans_id
            )
            .all()
        )

        return sum(
            d.haftalik_saat
            for d in sonuc
        )


def sinifa_gore_toplam_saat(cizelge_id, sinif):

    with DatabaseSession() as session:

        sonuc = (
            session.query(DersDetay)
            .filter(
                DersDetay.cizelge_id == cizelge_id,
                DersDetay.sinif == sinif
            )
            .all()
        )

        return sum(
            d.haftalik_saat
            for d in sonuc
        )


def alana_gore_subeler(alan_id):

    with DatabaseSession() as session:

        return (
            session.query(Sube)
            .filter(
                Sube.alan_id == alan_id,
                Sube.aktif == True
            )
            .order_by(
                Sube.sinif,
                Sube.sube
            )
            .all()
        )


# ==========================================================
# VERİTABANI BAKIM
# ==========================================================

def veritabani_yedekle():

    import shutil
    from pathlib import Path
    from datetime import datetime

    kaynak = Path("data/normasistan.db")

    hedef = Path(
        f"backup/normasistan_{datetime.now():%Y%m%d_%H%M%S}.db"
    )

    hedef.parent.mkdir(exist_ok=True)

    shutil.copy2(kaynak, hedef)

    return hedef


def veritabani_optimize():

    with engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as connection:

        connection.execute(text("VACUUM"))
        connection.execute(text("ANALYZE"))

    return True

# ==========================================================
# GERİYE DÖNÜK UYUMLULUK
# ==========================================================

def alan_sil(alan_id):
    return alan_pasif_yap(alan_id)


def brans_sil(brans_id):
    return brans_pasif_yap(brans_id)


def ders_sil(ders_id):
    return ders_pasif_yap(ders_id)


def cizelge_sil(cizelge_id):
    return cizelge_pasif_yap(cizelge_id)

# ==========================================================
# KONAKLAMA HİZMETLERİ DERS ÇİZELGESİ AKTARMA
# ==========================================================

def konaklama_hizmetleri_cizelgesini_aktar(yil):
    """
    Konaklama Hizmetleri Dalı Anadolu Meslek Programı
    haftalık ders çizelgesini veritabanına aktarır.

    Aynı yıl ve aynı çizelge yeniden aktarılırsa eski
    DersDetay kayıtları silinir ve güncel saatler yazılır.
    """

    try:
        yil = int(yil)
    except (TypeError, ValueError) as hata:
        raise ValueError(
            "Çizelge yılı sayısal bir değer olmalıdır."
        ) from hata

    cizelge_adi = (
        "Konaklama Hizmetleri Dalı "
        "Anadolu Meslek Programı Haftalık Ders Çizelgesi"
    )

    program_adi = "Anadolu Meslek Programı"

    # ders adı, kategori, seçmeli mi, sınıflara göre haftalık saat
    ders_verileri = [
        (
            "Türk Dili ve Edebiyatı",
            "Ortak Ders",
            False,
            {9: 5, 10: 4, 11: 4, 12: 4},
        ),
        (
            "Din Kültürü ve Ahlak Bilgisi",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 2, 12: 2},
        ),
        (
            "Tarih",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 2, 12: 0},
        ),
        (
            "T.C. İnkılap Tarihi ve Atatürkçülük",
            "Ortak Ders",
            False,
            {9: 0, 10: 0, 11: 0, 12: 2},
        ),
        (
            "Coğrafya",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 0, 12: 0},
        ),
        (
            "Matematik",
            "Ortak Ders",
            False,
            {9: 5, 10: 5, 11: 0, 12: 0},
        ),
        (
            "Fizik",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 0, 12: 0},
        ),
        (
            "Kimya",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 0, 12: 0},
        ),
        (
            "Biyoloji",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 0, 12: 0},
        ),
        (
            "Felsefe",
            "Ortak Ders",
            False,
            {9: 0, 10: 2, 11: 2, 12: 0},
        ),
        (
            "Yabancı Dil",
            "Ortak Ders",
            False,
            {9: 4, 10: 2, 11: 2, 12: 2},
        ),
        (
            "Beden Eğitimi ve Spor/Görsel Sanatlar/Müzik",
            "Ortak Ders",
            False,
            {9: 2, 10: 2, 11: 2, 12: 0},
        ),
        (
            "Sağlık Bilgisi ve Trafik Kültürü",
            "Ortak Ders",
            False,
            {9: 0, 10: 0, 11: 1, 12: 0},
        ),
        (
            "Mesleki Gelişim Atölyesi",
            "Meslek Dersi",
            False,
            {9: 2, 10: 0, 11: 0, 12: 0},
        ),
        (
            "Genel Turizm",
            "Meslek Dersi",
            False,
            {9: 3, 10: 0, 11: 0, 12: 0},
        ),
        (
            "Konaklama ve Seyahat Hizmetleri Atölyesi",
            "Meslek Dersi",
            False,
            {9: 6, 10: 0, 11: 0, 12: 0},
        ),
        (
            "Önbüroda Rezervasyon",
            "Meslek Dersi",
            False,
            {9: 0, 10: 2, 11: 0, 12: 0},
        ),
        (
            "Konuk Giriş Çıkış İşlemleri",
            "Meslek Dersi",
            False,
            {9: 0, 10: 2, 11: 0, 12: 0},
        ),
        (
            "Kat Hizmetleri Atölyesi",
            "Meslek Dersi",
            False,
            {9: 0, 10: 4, 11: 4, 12: 0},
        ),
        (
            "Önbüro Hizmetleri Atölyesi",
            "Meslek Dersi",
            False,
            {9: 0, 10: 5, 11: 5, 12: 0},
        ),
        (
            "Sürdürülebilir Turizm",
            "Meslek Dersi",
            False,
            {9: 0, 10: 0, 11: 2, 12: 0},
        ),
        (
            "Konaklama İşletmeciliği",
            "Meslek Dersi",
            False,
            {9: 0, 10: 0, 11: 3, 12: 0},
        ),
        (
            "Mesleki Yabancı Dil",
            "Meslek Dersi",
            False,
            {9: 0, 10: 0, 11: 3, 12: 0},
        ),
        (
            "İşletmelerde Mesleki Eğitim",
            "Meslek Dersi",
            False,
            {9: 0, 10: 0, 11: 0, 12: 24},
        ),
        (
            "Seçmeli Meslek Dersleri",
            "Seçmeli Ders",
            True,
            {9: 0, 10: 0, 11: 12, 12: 11},
        ),
        (
            "Seçmeli Dersler",
            "Seçmeli Ders",
            True,
            {9: 5, 10: 4, 11: 0, 12: 0},
        ),
        (
            "Rehberlik ve Yönlendirme",
            "Ortak Ders",
            False,
            {9: 0, 10: 1, 11: 1, 12: 0},
        ),
    ]

    with DatabaseSession() as session:

        cizelge = (
            session.query(DersCizelgesi)
            .filter(
                DersCizelgesi.adi == cizelge_adi,
                DersCizelgesi.yil == yil,
            )
            .first()
        )

        if cizelge is None:

            cizelge = DersCizelgesi(
                adi=cizelge_adi,
                program=program_adi,
                yil=yil,
                aktif=True,
            )

            session.add(cizelge)
            session.flush()

        else:

            cizelge.program = program_adi
            cizelge.aktif = True

            (
                session.query(DersDetay)
                .filter(
                    DersDetay.cizelge_id == cizelge.id
                )
                .delete(
                    synchronize_session=False
                )
            )

        yeni_eklenen_ders_sayisi = 0
        guncellenen_ders_sayisi = 0
        eklenen_detay_sayisi = 0

        for (
            ders_adi,
            kategori,
            secmeli,
            sinif_saatleri,
        ) in ders_verileri:

            ders = (
                session.query(Ders)
                .filter(
                    Ders.ders_adi.ilike(ders_adi)
                )
                .first()
            )

            if ders is None:

                ders = Ders(
                    ders_adi=ders_adi,
                    kategori=kategori,
                    brans_id=None,
                    secmeli=secmeli,
                    aktif=True,
                )

                session.add(ders)
                session.flush()

                yeni_eklenen_ders_sayisi += 1

            else:

                ders.kategori = kategori
                ders.secmeli = secmeli
                ders.aktif = True

                guncellenen_ders_sayisi += 1

            for sinif, haftalik_saat in sinif_saatleri.items():

                if haftalik_saat <= 0:
                    continue

                session.add(
                    DersDetay(
                        cizelge_id=cizelge.id,
                        ders_id=ders.id,
                        sinif=sinif,
                        haftalik_saat=haftalik_saat,
                        teorik=haftalik_saat,
                        uygulama=0,
                    )
                )

                eklenen_detay_sayisi += 1

        return {
            "basarili": True,
            "cizelge_id": cizelge.id,
            "cizelge_adi": cizelge_adi,
            "yil": yil,
            "eklenen_ders": yeni_eklenen_ders_sayisi,
            "guncellenen_ders": guncellenen_ders_sayisi,
            "eklenen_detay": eklenen_detay_sayisi,
        }
