from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
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
)

from database.database import (
    alanlari_getir,
    subeleri_getir,
    sube_ekle,
    sube_guncelle,
    sube_sil,
)


class SubelerPage(QWidget):
    """
    Şube kayıtlarının eklenmesi, güncellenmesi ve silinmesi için kullanılan sayfa.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.secili_sube_id = None
        self.alan_adlari = {}

        self.arayuzu_olustur()
        self.alanlari_yukle()
        self.subeleri_yukle()

    # ======================================================
    # ARAYÜZ
    # ======================================================

    def arayuzu_olustur(self):
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(15)

        baslik = QLabel("Şube Yönetimi")
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
            "Okuldaki sınıf ve şube bilgilerini ekleyebilir, "
            "güncelleyebilir veya silebilirsiniz."
        )
        aciklama.setWordWrap(True)
        ana_layout.addWidget(aciklama)

        # --------------------------------------------------
        # FORM
        # --------------------------------------------------

        form_grubu = QGroupBox("Şube Bilgileri")
        form_layout = QFormLayout(form_grubu)
        form_layout.setContentsMargins(15, 20, 15, 15)
        form_layout.setSpacing(12)

        self.sinif_combo = QComboBox()
        self.sinif_combo.addItem("Sınıf seçiniz", None)
        self.sinif_combo.addItem("9. Sınıf", 9)
        self.sinif_combo.addItem("10. Sınıf", 10)
        self.sinif_combo.addItem("11. Sınıf", 11)
        self.sinif_combo.addItem("12. Sınıf", 12)

        self.sube_combo = QComboBox()
        self.sube_combo.addItem("Şube seçiniz", None)

        for harf in [
            "A", "B", "C", "D", "E", "F", "G", "H",
            "I", "İ", "J", "K", "L", "M", "N", "O",
            "Ö", "P", "R", "S", "Ş", "T", "U", "Ü",
            "V", "Y", "Z"
        ]:
            self.sube_combo.addItem(harf, harf)

        self.alan_combo = QComboBox()
        self.alan_combo.addItem("Alan seçiniz", None)

        self.ogrenci_sayisi_input = QLineEdit()
        self.ogrenci_sayisi_input.setPlaceholderText("Örnek: 24")
        self.ogrenci_sayisi_input.setValidator(QIntValidator(0, 999, self))

        form_layout.addRow("Sınıf:", self.sinif_combo)
        form_layout.addRow("Şube:", self.sube_combo)
        form_layout.addRow("Alan:", self.alan_combo)
        form_layout.addRow("Öğrenci Sayısı:", self.ogrenci_sayisi_input)

        ana_layout.addWidget(form_grubu)

        # --------------------------------------------------
        # BUTONLAR
        # --------------------------------------------------

        buton_layout = QHBoxLayout()
        buton_layout.setSpacing(10)

        self.yeni_buton = QPushButton("Yeni")
        self.kaydet_buton = QPushButton("Kaydet")
        self.guncelle_buton = QPushButton("Güncelle")
        self.sil_buton = QPushButton("Sil")

        self.yeni_buton.clicked.connect(self.formu_temizle)
        self.kaydet_buton.clicked.connect(self.kaydet)
        self.guncelle_buton.clicked.connect(self.guncelle)
        self.sil_buton.clicked.connect(self.sil)

        self.guncelle_buton.setEnabled(False)
        self.sil_buton.setEnabled(False)

        buton_layout.addWidget(self.yeni_buton)
        buton_layout.addWidget(self.kaydet_buton)
        buton_layout.addWidget(self.guncelle_buton)
        buton_layout.addWidget(self.sil_buton)
        buton_layout.addStretch()

        ana_layout.addLayout(buton_layout)

        # --------------------------------------------------
        # TABLO
        # --------------------------------------------------

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(
            [
                "ID",
                "Sınıf",
                "Şube",
                "Alan",
                "Öğrenci Sayısı",
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

        basliklar = self.tablo.horizontalHeader()
        basliklar.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents,
        )
        basliklar.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents,
        )
        basliklar.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents,
        )
        basliklar.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.Stretch,
        )
        basliklar.setSectionResizeMode(
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

        self.durum_label = QLabel("")
        self.durum_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ana_layout.addWidget(self.durum_label)

    # ======================================================
    # ALANLAR
    # ======================================================

    def alanlari_yukle(self):
        """
        Alanları açılır listeye yükler.

        Alan adları ayrıca alan_id: alan_adi biçiminde sözlükte tutulur.
        Böylece SQLAlchemy relationship kullanılmadan alan adı tabloda
        güvenli biçimde gösterilir.
        """

        try:
            alanlar = alanlari_getir()

            self.alan_combo.blockSignals(True)
            self.alan_combo.clear()
            self.alan_combo.addItem("Alan seçiniz", None)

            self.alan_adlari.clear()

            for alan in alanlar:
                alan_id = getattr(alan, "id", None)
                alan_adi = getattr(alan, "alan_adi", "")

                if alan_id is None:
                    continue

                self.alan_adlari[alan_id] = alan_adi
                self.alan_combo.addItem(alan_adi, alan_id)

            self.alan_combo.blockSignals(False)

        except Exception as hata:
            self.alan_combo.blockSignals(False)

            QMessageBox.critical(
                self,
                "Alanlar Yüklenemedi",
                f"Alan kayıtları yüklenirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # ŞUBELER
    # ======================================================

    def subeleri_yukle(self):
        """
        Aktif şubeleri veritabanından okuyarak tabloya yükler.
        """

        try:
            subeler = subeleri_getir()

            self.tablo.setRowCount(0)

            for kayit in subeler:
                satir = self.tablo.rowCount()
                self.tablo.insertRow(satir)

                sube_id = getattr(kayit, "id", "")
                sinif = getattr(kayit, "sinif", "")
                sube = getattr(kayit, "sube", "")
                alan_id = getattr(kayit, "alan_id", None)
                ogrenci_sayisi = getattr(
                    kayit,
                    "ogrenci_sayisi",
                    0,
                )

                alan_adi = self.alan_adlari.get(
                    alan_id,
                    "Alan belirtilmemiş",
                )

                id_item = QTableWidgetItem(str(sube_id))
                sinif_item = QTableWidgetItem(str(sinif))
                sube_item = QTableWidgetItem(str(sube))
                alan_item = QTableWidgetItem(str(alan_adi))
                ogrenci_item = QTableWidgetItem(
                    str(ogrenci_sayisi)
                )

                id_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                sinif_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                sube_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                ogrenci_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                # Satır seçildiğinde alan_id bilgisine erişebilmek için
                # ID hücresinde özel veri olarak saklanır.
                id_item.setData(
                    Qt.ItemDataRole.UserRole,
                    alan_id,
                )

                self.tablo.setItem(satir, 0, id_item)
                self.tablo.setItem(satir, 1, sinif_item)
                self.tablo.setItem(satir, 2, sube_item)
                self.tablo.setItem(satir, 3, alan_item)
                self.tablo.setItem(satir, 4, ogrenci_item)

            self.durum_label.setText(
                f"Toplam {len(subeler)} aktif şube bulunmaktadır."
            )

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Şubeler Yüklenemedi",
                f"Şube kayıtları yüklenirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # FORM İŞLEMLERİ
    # ======================================================

    def form_verilerini_al(self):
        """
        Formdaki bilgileri doğrular ve sözlük olarak döndürür.
        Hatalı giriş varsa None döndürür.
        """

        sinif = self.sinif_combo.currentData()
        sube = self.sube_combo.currentData()
        alan_id = self.alan_combo.currentData()
        ogrenci_metni = self.ogrenci_sayisi_input.text().strip()

        if sinif is None:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen sınıf seçiniz.",
            )
            self.sinif_combo.setFocus()
            return None

        if not sube:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen şube adını giriniz.",
            )
            self.sube_input.setFocus()
            return None

        if alan_id is None:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen alan seçiniz.",
            )
            self.alan_combo.setFocus()
            return None

        if not ogrenci_metni:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen öğrenci sayısını giriniz.",
            )
            self.ogrenci_sayisi_input.setFocus()
            return None

        try:
            ogrenci_sayisi = int(ogrenci_metni)
        except ValueError:
            QMessageBox.warning(
                self,
                "Hatalı Bilgi",
                "Öğrenci sayısı sayısal bir değer olmalıdır.",
            )
            self.ogrenci_sayisi_input.setFocus()
            return None

        if ogrenci_sayisi < 0:
            QMessageBox.warning(
                self,
                "Hatalı Bilgi",
                "Öğrenci sayısı sıfırdan küçük olamaz.",
            )
            return None

        return {
            "sinif": sinif,
            "sube": sube,
            "alan_id": alan_id,
            "ogrenci_sayisi": ogrenci_sayisi,
        }

    def formu_temizle(self):
        self.secili_sube_id = None

        self.sinif_combo.setCurrentIndex(0)
        self.sube_combo.setCurrentIndex(0)
        self.alan_combo.setCurrentIndex(0)
        self.ogrenci_sayisi_input.clear()

        self.tablo.clearSelection()

        self.kaydet_buton.setEnabled(True)
        self.guncelle_buton.setEnabled(False)
        self.sil_buton.setEnabled(False)

        self.sube_combo.setFocus()

    def secili_satiri_forma_aktar(self, *args):
        secili_satirlar = self.tablo.selectionModel().selectedRows()

        if not secili_satirlar:
            return

        satir = secili_satirlar[0].row()

        id_item = self.tablo.item(satir, 0)
        sinif_item = self.tablo.item(satir, 1)
        sube_item = self.tablo.item(satir, 2)
        ogrenci_item = self.tablo.item(satir, 4)

        if id_item is None:
            return

        try:
            self.secili_sube_id = int(id_item.text())
        except (TypeError, ValueError):
            self.secili_sube_id = None
            return

        alan_id = id_item.data(Qt.ItemDataRole.UserRole)

        try:
            sinif = int(sinif_item.text())
        except (TypeError, ValueError):
            sinif = None

        sinif_index = self.sinif_combo.findData(sinif)

        if sinif_index >= 0:
            self.sinif_combo.setCurrentIndex(sinif_index)
        else:
            self.sinif_combo.setCurrentIndex(0)

        sube_degeri = sube_item.text() if sube_item else None
        sube_index = self.sube_combo.findData(sube_degeri)

        if sube_index >= 0:
            self.sube_combo.setCurrentIndex(sube_index)
        else:
            self.sube_combo.setCurrentIndex(0)

        alan_index = self.alan_combo.findData(alan_id)

        if alan_index >= 0:
            self.alan_combo.setCurrentIndex(alan_index)
        else:
            self.alan_combo.setCurrentIndex(0)

        self.ogrenci_sayisi_input.setText(
            ogrenci_item.text() if ogrenci_item else "0"
        )

        self.kaydet_buton.setEnabled(False)
        self.guncelle_buton.setEnabled(True)
        self.sil_buton.setEnabled(True)

    # ======================================================
    # KAYDET
    # ======================================================

    def kaydet(self):
        veriler = self.form_verilerini_al()

        if veriler is None:
            return

        try:
            sonuc = sube_ekle(
                sinif=veriler["sinif"],
                sube=veriler["sube"],
                alan_id=veriler["alan_id"],
                ogrenci_sayisi=veriler["ogrenci_sayisi"],
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Kayıt Yapılamadı",
                    "Şube kaydı oluşturulamadı.",
                )
                return

            QMessageBox.information(
                self,
                "Kayıt Başarılı",
                "Şube başarıyla kaydedildi.",
            )

            self.alanlari_yukle()
            self.subeleri_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Kayıt Hatası",
                f"Şube kaydedilirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # GÜNCELLE
    # ======================================================

    def guncelle(self):
        if self.secili_sube_id is None:
            QMessageBox.warning(
                self,
                "Kayıt Seçilmedi",
                "Güncellemek istediğiniz şubeyi tablodan seçiniz.",
            )
            return

        veriler = self.form_verilerini_al()

        if veriler is None:
            return

        try:
            sonuc = sube_guncelle(
                sube_id=self.secili_sube_id,
                sinif=veriler["sinif"],
                sube=veriler["sube"],
                alan_id=veriler["alan_id"],
                ogrenci_sayisi=veriler["ogrenci_sayisi"],
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Güncelleme Yapılamadı",
                    "Şube kaydı bulunamadı veya güncellenemedi.",
                )
                return

            QMessageBox.information(
                self,
                "Güncelleme Başarılı",
                "Şube bilgileri başarıyla güncellendi.",
            )

            self.alanlari_yukle()
            self.subeleri_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Güncelleme Hatası",
                f"Şube güncellenirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # SİL
    # ======================================================

    def sil(self):
        if self.secili_sube_id is None:
            QMessageBox.warning(
                self,
                "Kayıt Seçilmedi",
                "Silmek istediğiniz şubeyi tablodan seçiniz.",
            )
            return

        cevap = QMessageBox.question(
            self,
            "Şubeyi Sil",
            "Seçili şube kaydını silmek istediğinizden emin misiniz?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if cevap != QMessageBox.StandardButton.Yes:
            return

        try:
            sonuc = sube_sil(self.secili_sube_id)

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Silme Yapılamadı",
                    "Şube kaydı bulunamadı veya silinemedi.",
                )
                return

            QMessageBox.information(
                self,
                "Silme Başarılı",
                "Şube kaydı başarıyla silindi.",
            )

            self.alanlari_yukle()
            self.subeleri_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Silme Hatası",
                f"Şube silinirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # SAYFA YENİLEME
    # ======================================================

    def yenile(self):
        """
        Ana pencereden ihtiyaç duyulması hâlinde çağrılabilir.
        """

        self.alanlari_yukle()
        self.subeleri_yukle()
        self.formu_temizle()