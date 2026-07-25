from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QGroupBox,
    QAbstractItemView,
)

from database.database import (
    branslari_getir,
    brans_ekle,
    brans_guncelle,
    brans_sil,
)


class BranslarPage(QWidget):
    """
    Branş kayıtlarının eklenmesi, güncellenmesi ve silinmesi
    için kullanılan yönetim ekranı.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.secili_brans_id = None

        self.arayuzu_olustur()
        self.branslari_yukle()

    # ======================================================
    # ARAYÜZ
    # ======================================================

    def arayuzu_olustur(self):
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(20, 20, 20, 20)
        ana_layout.setSpacing(15)

        baslik = QLabel("Branş Yönetimi")
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
            "Okulda bulunan öğretmen branşlarını ve MEB kodlarını "
            "ekleyebilir, güncelleyebilir veya silebilirsiniz."
        )
        aciklama.setWordWrap(True)
        ana_layout.addWidget(aciklama)

        # --------------------------------------------------
        # FORM
        # --------------------------------------------------

        form_grubu = QGroupBox("Branş Bilgileri")
        form_layout = QFormLayout(form_grubu)
        form_layout.setContentsMargins(15, 20, 15, 15)
        form_layout.setSpacing(12)

        self.meb_kodu_input = QLineEdit()
        self.meb_kodu_input.setPlaceholderText("Örnek: 101")
        self.meb_kodu_input.setMaxLength(20)

        self.brans_adi_input = QLineEdit()
        self.brans_adi_input.setPlaceholderText("Örnek: Matematik")
        self.brans_adi_input.setMaxLength(150)

        form_layout.addRow("MEB Kodu:", self.meb_kodu_input)
        form_layout.addRow("Branş Adı:", self.brans_adi_input)

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
        self.tablo.setColumnCount(3)

        self.tablo.setHorizontalHeaderLabels(
            [
                "ID",
                "Branş Adı",
                "MEB Kodu",
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

        self.tablo.itemSelectionChanged.connect(
            self.secili_satiri_forma_aktar
        )

        self.tablo.cellDoubleClicked.connect(
            self.secili_satiri_forma_aktar
        )

        ana_layout.addWidget(self.tablo)

        self.durum_label = QLabel("")
        self.durum_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        ana_layout.addWidget(self.durum_label)

    # ======================================================
    # BRANŞLARI YÜKLE
    # ======================================================

    def branslari_yukle(self):
        try:
            branslar = branslari_getir()

            # database.py sıralamasından bağımsız olarak
            # ID küçükten büyüğe sıralanır.
            branslar = sorted(
                branslar,
                key=lambda kayit: getattr(kayit, "id", 0),
            )

            self.tablo.setRowCount(0)

            for brans in branslar:
                satir = self.tablo.rowCount()
                self.tablo.insertRow(satir)

                brans_id = getattr(brans, "id", "")
                brans_adi = getattr(brans, "brans_adi", "")
                meb_kodu = getattr(brans, "meb_kodu", "")

                if meb_kodu is None:
                    meb_kodu = ""

                id_item = QTableWidgetItem(str(brans_id))
                brans_adi_item = QTableWidgetItem(str(brans_adi))
                meb_kodu_item = QTableWidgetItem(str(meb_kodu))

                id_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                meb_kodu_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.tablo.setItem(
                    satir,
                    0,
                    id_item,
                )

                self.tablo.setItem(
                    satir,
                    1,
                    brans_adi_item,
                )

                self.tablo.setItem(
                    satir,
                    2,
                    meb_kodu_item,
                )

            self.durum_label.setText(
                f"Toplam Branş: {len(branslar)}"
            )

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Branşlar Yüklenemedi",
                f"Branş kayıtları yüklenirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # FORM VERİLERİ
    # ======================================================

    def form_verilerini_al(self):
        meb_kodu = self.meb_kodu_input.text().strip()
        brans_adi = self.brans_adi_input.text().strip()

        if not brans_adi:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen branş adını giriniz.",
            )

            self.brans_adi_input.setFocus()
            return None

        return {
            "meb_kodu": meb_kodu,
            "brans_adi": brans_adi,
        }

    # ======================================================
    # FORM TEMİZLE
    # ======================================================

    def formu_temizle(self):
        self.secili_brans_id = None

        self.meb_kodu_input.clear()
        self.brans_adi_input.clear()

        self.tablo.clearSelection()

        self.kaydet_buton.setEnabled(True)
        self.guncelle_buton.setEnabled(False)
        self.sil_buton.setEnabled(False)

        self.meb_kodu_input.setFocus()

    # ======================================================
    # SEÇİLİ SATIRI FORMA AKTAR
    # ======================================================

    def secili_satiri_forma_aktar(self, *args):
        secili_satirlar = self.tablo.selectionModel().selectedRows()

        if not secili_satirlar:
            return

        satir = secili_satirlar[0].row()

        id_item = self.tablo.item(satir, 0)
        brans_adi_item = self.tablo.item(satir, 1)
        meb_kodu_item = self.tablo.item(satir, 2)

        if id_item is None:
            return

        try:
            self.secili_brans_id = int(id_item.text())

        except (TypeError, ValueError):
            self.secili_brans_id = None
            return

        self.brans_adi_input.setText(
            brans_adi_item.text()
            if brans_adi_item is not None
            else ""
        )

        self.meb_kodu_input.setText(
            meb_kodu_item.text()
            if meb_kodu_item is not None
            else ""
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
            sonuc = brans_ekle(
                brans_adi=veriler["brans_adi"],
                meb_kodu=veriler["meb_kodu"],
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Kayıt Yapılamadı",
                    "Bu branş daha önce kaydedilmiş olabilir.",
                )
                return

            QMessageBox.information(
                self,
                "Kayıt Başarılı",
                "Branş başarıyla kaydedildi.",
            )

            self.branslari_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Kayıt Hatası",
                f"Branş kaydedilirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # GÜNCELLE
    # ======================================================

    def guncelle(self):
        if self.secili_brans_id is None:
            QMessageBox.warning(
                self,
                "Kayıt Seçilmedi",
                "Güncellemek istediğiniz branşı tablodan seçiniz.",
            )
            return

        veriler = self.form_verilerini_al()

        if veriler is None:
            return

        try:
            sonuc = brans_guncelle(
                brans_id=self.secili_brans_id,
                brans_adi=veriler["brans_adi"],
                meb_kodu=veriler["meb_kodu"],
            )

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Güncelleme Yapılamadı",
                    "Branş kaydı bulunamadı veya güncellenemedi.",
                )
                return

            QMessageBox.information(
                self,
                "Güncelleme Başarılı",
                "Branş bilgileri başarıyla güncellendi.",
            )

            self.branslari_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Güncelleme Hatası",
                f"Branş güncellenirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # SİL
    # ======================================================

    def sil(self):
        if self.secili_brans_id is None:
            QMessageBox.warning(
                self,
                "Kayıt Seçilmedi",
                "Silmek istediğiniz branşı tablodan seçiniz.",
            )
            return

        cevap = QMessageBox.question(
            self,
            "Branşı Sil",
            "Seçili branşı silmek istediğinizden emin misiniz?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if cevap != QMessageBox.StandardButton.Yes:
            return

        try:
            sonuc = brans_sil(self.secili_brans_id)

            if not sonuc:
                QMessageBox.warning(
                    self,
                    "Silme Yapılamadı",
                    "Branş kaydı bulunamadı veya silinemedi.",
                )
                return

            QMessageBox.information(
                self,
                "Silme Başarılı",
                "Branş başarıyla silindi.",
            )

            self.branslari_yukle()
            self.formu_temizle()

        except Exception as hata:
            QMessageBox.critical(
                self,
                "Silme Hatası",
                f"Branş silinirken hata oluştu:\n\n{hata}",
            )

    # ======================================================
    # SAYFA YENİLE
    # ======================================================

    def yenile(self):
        self.branslari_yukle()
        self.formu_temizle()