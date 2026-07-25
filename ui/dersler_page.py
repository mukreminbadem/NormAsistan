from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QGroupBox,
    QAbstractItemView,
    QInputDialog,
)

from database.database import (
    branslari_getir,
    dersleri_getir,
    ders_ekle,
    ders_guncelle,
    ders_sil,
    konaklama_hizmetleri_cizelgesini_aktar,
)


class DerslerPage(QWidget):
    """
    Ders kayıtlarının eklenmesi, güncellenmesi, silinmesi
    ve hazır haftalık ders çizelgelerinin aktarılması için
    kullanılan yönetim ekranı.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.secili_ders_id = None
        self.brans_adlari = {}

        self.arayuzu_olustur()
        self.branslari_yukle()
        self.dersleri_yukle()

    # ======================================================
    # ARAYÜZ
    # ======================================================

    def arayuzu_olustur(self):
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(15)

        # --------------------------------------------------
        # BAŞLIK
        # --------------------------------------------------

        baslik = QLabel("Ders Yönetimi")
        baslik.setStyleSheet(
            """
            QLabel {
                font-size: 22px;
                font-weight: bold;
            }
            """
        )

        ana_layout.addWidget(baslik)

        aciklama = QLabel(
            "Okulda okutulan ortak, meslek ve seçmeli dersleri "
            "ekleyebilir, güncelleyebilir veya silebilirsiniz. "
            "Hazır ders çizelgesi aktarma düğmesiyle çizelgedeki "
            "dersleri ve haftalık ders saatlerini otomatik olarak "
            "veritabanına aktarabilirsiniz."
        )

        aciklama.setWordWrap(True)
        ana_layout.addWidget(aciklama)

        # --------------------------------------------------
        # FORM
        # --------------------------------------------------

        form_grubu = QGroupBox("Ders Bilgileri")

        form_layout = QFormLayout(form_grubu)
        form_layout.setContentsMargins(15, 20, 15, 15)
        form_layout.setSpacing(12)

        self.ders_adi_input = QLineEdit()
        self.ders_adi_input.setPlaceholderText(
            "Örnek: Türk Dili ve Edebiyatı"
        )
        self.ders_adi_input.setMaxLength(200)

        self.kategori_combo = QComboBox()
        self.kategori_combo.addItem(
            "Kategori seçiniz",
            None,
        )
        self.kategori_combo.addItem(
            "Ortak Ders",
            "Ortak Ders",
        )
        self.kategori_combo.addItem(
            "Meslek Dersi",
            "Meslek Dersi",
        )
        self.kategori_combo.addItem(
            "Seçmeli Ders",
            "Seçmeli Ders",
        )

        self.brans_combo = QComboBox()
        self.brans_combo.addItem(
            "Branş seçiniz",
            None,
        )

        form_layout.addRow(
            "Ders Adı:",
            self.ders_adi_input,
        )

        form_layout.addRow(
            "Kategori:",
            self.kategori_combo,
        )

        form_layout.addRow(
            "Branş:",
            self.brans_combo,
        )

        ana_layout.addWidget(form_grubu)

        # --------------------------------------------------
        # İŞLEM DÜĞMELERİ
        # --------------------------------------------------

        buton_layout = QHBoxLayout()
        buton_layout.setSpacing(10)

        self.yeni_buton = QPushButton("Yeni")
        self.kaydet_buton = QPushButton("Kaydet")
        self.guncelle_buton = QPushButton("Güncelle")
        self.sil_buton = QPushButton("Sil")

        self.cizelge_aktar_buton = QPushButton(
            "Konaklama Çizelgesini Aktar"
        )

        self.yeni_buton.clicked.connect(
            self.formu_temizle
        )

        self.kaydet_buton.clicked.connect(
            self.kaydet
        )

        self.guncelle_buton.clicked.connect(
            self.guncelle
        )

        self.sil_buton.clicked.connect(
            self.sil
        )

        self.cizelge_aktar_buton.clicked.connect(
            self.konaklama_cizelgesini_aktar
        )

        self.guncelle_buton.setEnabled(False)
        self.sil_buton.setEnabled(False)

        buton_layout.addWidget(
            self.yeni_buton
        )

        buton_layout.addWidget(
            self.kaydet_buton
        )

        buton_layout.addWidget(
            self.guncelle_buton
        )

        buton_layout.addWidget(
            self.sil_buton
        )

        buton_layout.addStretch()

        buton_layout.addWidget(
            self.cizelge_aktar_buton
        )

        ana_layout.addLayout(buton_layout)

        # --------------------------------------------------
        # TABLO
        # --------------------------------------------------

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)

        self.tablo.setHorizontalHeaderLabels(
            [
                "ID",
                "Ders Adı",
                "Kategori",
                "Branş",
                "Seçmeli",
            ]
        )

        self.tablo.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tablo.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tablo.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tablo.setAlternatingRowColors(True)
        self.tablo.setSortingEnabled(False)
        self.tablo.verticalHeader().setVisible(False)

        header = self.tablo.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.Stretch,
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self.tablo.itemSelectionChanged.connect(
            self.secili_satiri_forma_aktar
        )

        self.tablo.cellDoubleClicked.connect(
            self.secili_satiri_forma_aktar
        )

        ana_layout.addWidget(self.tablo)

        # --------------------------------------------------
        # DURUM BİLGİSİ
        # --------------------------------------------------

        self.durum_label = QLabel("")
        self.durum_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        ana_layout.addWidget(
            self.durum_label
        )

    # ======================================================
    # BRANŞLARI YÜKLE
    # ======================================================

    def branslari_yukle(self):
        """
        Aktif branşları açılır kutuya yükler.

        Branş adları ayrıca branş ID'si ile eşleştirilir.
        Böylece Ders modelindeki relationship bağlantısına
        ihtiyaç duyulmadan branş adı tabloda gösterilebilir.
        """

        try:
            mevcut_brans_id = self.brans_combo.currentData()

            branslar = branslari_getir()

            branslar = sorted(
                branslar,
                key=lambda kayit: getattr(
                    kayit,
                    "id",
                    0,
                ),
            )

            self.brans_combo.blockSignals(True)
            self.brans_combo.clear()

            self.brans_combo.addItem(
                "Branş seçiniz",
                None,
            )

            self.brans_adlari.clear()

            for brans in branslar:
                brans_id = getattr(
                    brans,
                    "id",
                    None,
                )

                brans_adi = getattr(
                    brans,
                    "brans_adi",
                    "",
                )

                if brans_id is None:
                    continue

                self.brans_adlari[brans_id] = brans_adi

                self.brans_combo.addItem(
                    brans_adi,
                    brans_id,
                )

            if mevcut_brans_id is not None:
                index = self.brans_combo.findData(
                    mevcut_brans_id
                )

                if index >= 0:
                    self.brans_combo.setCurrentIndex(
                        index
                    )

            self.brans_combo.blockSignals(False)

        except Exception as hata:
            self.brans_combo.blockSignals(False)

            QMessageBox.critical(
                self,
                "Branşlar Yüklenemedi",
                (
                    "Branş kayıtları yüklenirken "
                    f"hata oluştu:\n\n{hata}"
                ),
            )

    # ======================================================
    # DERSLERİ YÜKLE
    # ======================================================

    def dersleri_yukle(self):
        """
        Aktif dersleri ID küçükten büyüğe sıralayarak
        tabloya yükler.
        """

        try:
            dersler = dersleri_getir()

            dersler = sorted(
                dersler,
                key=lambda kayit: getattr(
                    kayit,
                    "id",
                    0,
                ),
            )

            self.tablo.setRowCount(0)

            for ders in dersler:
                satir = self.tablo.rowCount()
                self.tablo.insertRow(satir)

                ders_id = getattr(
                    ders,
                    "id",
                    "",
                )

                ders_adi = getattr(
                    ders,
                    "ders_adi",
                    "",
                )

                kategori = getattr(
                    ders,
                    "kategori",
                    "",
                )

                brans_id = getattr(
                    ders,
                    "brans_id",
                    None,
                )

                secmeli = bool(
                    getattr(
                        ders,
                        "secmeli",
                        False,
                    )
                )

                if brans_id is None:
                    brans_adi = "Branş belirtilmemiş"
                else:
                    brans_adi = self.brans_adlari.get(
                        brans_id,
                        "Branş bulunamadı",
                    )

                secmeli_metni = (
                    "Evet"
                    if secmeli
                    else "Hayır"
                )

                id_item = QTableWidgetItem(
                    str(ders_id)
                )

                ders_adi_item = QTableWidgetItem(
                    str(ders_adi)
                )

                kategori_item = QTableWidgetItem(
                    str(kategori)
                )

                brans_item = QTableWidgetItem(
                    str(brans_adi)
                )

                secmeli_item = QTableWidgetItem(
                    secmeli_metni
                )

                id_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                kategori_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                secmeli_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                # Ders satırında branş ID bilgisini saklıyoruz.
                # Satır seçildiğinde doğru branş açılır kutudan
                # otomatik olarak seçilecektir.
                id_item.setData(
                    Qt.ItemDataRole.UserRole,
                    brans_id,
                )

                self.tablo.setItem(
                    satir,
                    0,
                    id_item,
                )

                self.tablo.setItem(
                    satir,
                    1,
                    ders_adi_item,
                )

                self.tablo.setItem(
                    satir,
                    2,
                    kategori_item,
                )

                self.tablo.setItem(
                    satir,
                    3,
                    brans_item,
                )

                self.tablo.setItem(
                    satir,
                    4,
                    secmeli_item,
                )

            self.durum_label.setText(
                f"Toplam Ders: {len(dersler)}"
            )

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Dersler Yüklenemedi",
                (
                    "Ders kayıtları yüklenirken "
                    f"hata oluştu:\n\n{hata}"
                ),
            )

    # ======================================================
    # FORM VERİLERİNİ AL
    # ======================================================

    def form_verilerini_al(self):
        ders_adi = (
            self.ders_adi_input
            .text()
            .strip()
        )

        kategori = (
            self.kategori_combo
            .currentData()
        )

        brans_id = (
            self.brans_combo
            .currentData()
        )

        if not ders_adi:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen ders adını giriniz.",
            )

            self.ders_adi_input.setFocus()
            return None

        if kategori is None:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen ders kategorisini seçiniz.",
            )

            self.kategori_combo.setFocus()
            return None

        if brans_id is None:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen dersin ait olduğu branşı seçiniz.",
            )

            self.brans_combo.setFocus()
            return None

        secmeli = kategori == "Seçmeli Ders"

        return {
            "ders_adi": ders_adi,
            "kategori": kategori,
            "brans_id": brans_id,
            "secmeli": secmeli,
        }

    # ======================================================
    # FORMU TEMİZLE
    # ======================================================

    def formu_temizle(self):
        self.secili_ders_id = None

        self.ders_adi_input.clear()
        self.kategori_combo.setCurrentIndex(0)
        self.brans_combo.setCurrentIndex(0)

        self.tablo.clearSelection()

        self.kaydet_buton.setEnabled(True)
        self.guncelle_buton.setEnabled(False)
        self.sil_buton.setEnabled(False)

        self.ders_adi_input.setFocus()

    # ======================================================
    # SEÇİLİ SATIRI FORMA AKTAR
    # ======================================================

    def secili_satiri_forma_aktar(self, *args):
        secili_satirlar = (
            self.tablo
            .selectionModel()
            .selectedRows()
        )

        if not secili_satirlar:
            return

        satir = secili_satirlar[0].row()

        id_item = self.tablo.item(
            satir,
            0,
        )

        ders_adi_item = self.tablo.item(
            satir,
            1,
        )

        kategori_item = self.tablo.item(
            satir,
            2,
        )

        if id_item is None:
            return

        try:
            self.secili_ders_id = int(
                id_item.text()
            )

        except (TypeError, ValueError):
            self.secili_ders_id = None
            return

        brans_id = id_item.data(
            Qt.ItemDataRole.UserRole
        )

        ders_adi = (
            ders_adi_item.text()
            if ders_adi_item is not None
            else ""
        )

        kategori = (
            kategori_item.text()
            if kategori_item is not None
            else ""
        )

        self.ders_adi_input.setText(
            ders_adi
        )

        kategori_index = (
            self.kategori_combo.findData(
                kategori
            )
        )

        if kategori_index >= 0:
            self.kategori_combo.setCurrentIndex(
                kategori_index
            )
        else:
            self.kategori_combo.setCurrentIndex(0)

        brans_index = (
            self.brans_combo.findData(
                brans_id
            )
        )

        if brans_index >= 0:
            self.brans_combo.setCurrentIndex(
                brans_index
            )
        else:
            self.brans_combo.setCurrentIndex(0)

        self.kaydet_buton.setEnabled(False)
        self.guncelle_buton.setEnabled(True)
        self.sil_buton.setEnabled(True)

    # ======================================================
    # YENİ DERS KAYDET
    # ======================================================

    def kaydet(self):
        veriler = self.form_verilerini_al()

        if veriler is None:
            return

        try:
            sonuc = ders_ekle(
                ders_adi=veriler["ders_adi"],
                kategori=veriler["kategori"],
                brans_id=veriler["brans_id"],
                secmeli=veriler["secmeli"],
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Kayıt Yapılamadı",
                    "Ders kaydı oluşturulamadı.",
                )

                return

            QMessageBox.information(
                self,
                "Kayıt Başarılı",
                "Ders başarıyla kaydedildi.",
            )

            self.branslari_yukle()
            self.dersleri_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Kayıt Hatası",
                (
                    "Ders kaydedilirken "
                    f"hata oluştu:\n\n{hata}"
                ),
            )

    # ======================================================
    # DERS GÜNCELLE
    # ======================================================

    def guncelle(self):
        if self.secili_ders_id is None:
            QMessageBox.warning(
                self,
                "Kayıt Seçilmedi",
                (
                    "Güncellemek istediğiniz "
                    "dersi tablodan seçiniz."
                ),
            )

            return

        veriler = self.form_verilerini_al()

        if veriler is None:
            return

        try:
            sonuc = ders_guncelle(
                ders_id=self.secili_ders_id,
                ders_adi=veriler["ders_adi"],
                kategori=veriler["kategori"],
                brans_id=veriler["brans_id"],
                secmeli=veriler["secmeli"],
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Güncelleme Yapılamadı",
                    (
                        "Ders kaydı bulunamadı "
                        "veya güncellenemedi."
                    ),
                )

                return

            QMessageBox.information(
                self,
                "Güncelleme Başarılı",
                (
                    "Ders bilgileri başarıyla "
                    "güncellendi."
                ),
            )

            self.branslari_yukle()
            self.dersleri_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Güncelleme Hatası",
                (
                    "Ders güncellenirken "
                    f"hata oluştu:\n\n{hata}"
                ),
            )

    # ======================================================
    # DERS SİL
    # ======================================================

    def sil(self):
        if self.secili_ders_id is None:
            QMessageBox.warning(
                self,
                "Kayıt Seçilmedi",
                (
                    "Silmek istediğiniz "
                    "dersi tablodan seçiniz."
                ),
            )

            return

        cevap = QMessageBox.question(
            self,
            "Dersi Sil",
            (
                "Seçili dersi silmek "
                "istediğinizden emin misiniz?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if cevap != QMessageBox.StandardButton.Yes:
            return

        try:
            sonuc = ders_sil(
                self.secili_ders_id
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Silme Yapılamadı",
                    (
                        "Ders kaydı bulunamadı "
                        "veya silinemedi."
                    ),
                )

                return

            QMessageBox.information(
                self,
                "Silme Başarılı",
                "Ders başarıyla silindi.",
            )

            self.branslari_yukle()
            self.dersleri_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Silme Hatası",
                (
                    "Ders silinirken "
                    f"hata oluştu:\n\n{hata}"
                ),
            )

    # ======================================================
    # KONAKLAMA ÇİZELGESİNİ AKTAR
    # ======================================================

    def konaklama_cizelgesini_aktar(self):
        """
        Konaklama Hizmetleri Dalı Anadolu Meslek Programı
        haftalık ders çizelgesini seçilen yıl için aktarır.
        """

        yil, tamam = QInputDialog.getInt(
            self,
            "Ders Çizelgesi Yılı",
            (
                "Ders çizelgesinin uygulanacağı "
                "yılı giriniz:"
            ),
            2026,
            2000,
            2100,
            1,
        )

        if not tamam:
            return

        cevap = QMessageBox.question(
            self,
            "Ders Çizelgesini Aktar",
            (
                "Konaklama Hizmetleri Dalı Anadolu Meslek "
                "Programı haftalık ders çizelgesi "
                "veritabanına aktarılacaktır.\n\n"
                "Ders adları ve 9, 10, 11 ve 12. sınıf "
                "haftalık ders saatleri kaydedilecektir.\n\n"
                "Aynı yıla ait çizelge daha önce "
                "aktarılmışsa eski ders saati kayıtları "
                "silinerek yeniden oluşturulacaktır.\n\n"
                "İşleme devam edilsin mi?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No,
        )

        if cevap != QMessageBox.StandardButton.Yes:
            return

        try:
            self.cizelge_aktar_buton.setEnabled(False)
            self.cizelge_aktar_buton.setText(
                "Çizelge Aktarılıyor..."
            )

            sonuc = (
                konaklama_hizmetleri_cizelgesini_aktar(
                    yil=yil
                )
            )

            self.branslari_yukle()
            self.dersleri_yukle()
            self.formu_temizle()

            cizelge_adi = sonuc.get(
                "cizelge_adi",
                (
                    "Konaklama Hizmetleri Dalı "
                    "Haftalık Ders Çizelgesi"
                ),
            )

            eklenen_ders = sonuc.get(
                "eklenen_ders",
                0,
            )

            eklenen_detay = sonuc.get(
                "eklenen_detay",
                0,
            )

            QMessageBox.information(
                self,
                "Aktarma Tamamlandı",
                (
                    "Ders çizelgesi başarıyla aktarıldı.\n\n"
                    f"Yıl: {yil}\n"
                    f"Çizelge: {cizelge_adi}\n"
                    f"Yeni eklenen ders sayısı: "
                    f"{eklenen_ders}\n"
                    f"Aktarılan ders-sınıf saati kaydı: "
                    f"{eklenen_detay}\n\n"
                    "Aktarılan derslerin branşlarını "
                    "Ders Yönetimi ekranından seçerek "
                    "güncelleyebilirsiniz."
                ),
            )

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Aktarma Hatası",
                (
                    "Ders çizelgesi aktarılırken "
                    f"bir hata oluştu:\n\n{hata}"
                ),
            )

        finally:
            self.cizelge_aktar_buton.setEnabled(True)
            self.cizelge_aktar_buton.setText(
                "Konaklama Çizelgesini Aktar"
            )

    # ======================================================
    # SAYFAYI YENİLE
    # ======================================================

    def yenile(self):
        """
        Dersler sayfası sol menüden her açıldığında
        güncel branş ve ders kayıtlarını yeniden yükler.
        """

        self.branslari_yukle()
        self.dersleri_yukle()
        self.formu_temizle()