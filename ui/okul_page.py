from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QMessageBox
)

from database.database import (
    okul_getir,
    okul_kaydet
)


class OkulPage(QWidget):

    def __init__(self):
        super().__init__()

        self.arayuz_olustur()
        self.verileri_yukle()

    # ------------------------------------------------------
    # ARAYÜZ
    # ------------------------------------------------------

    def arayuz_olustur(self):

        layout = QVBoxLayout(self)

        baslik = QLabel("🏫 Okul Bilgileri")
        baslik.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(baslik)

        form = QFormLayout()

        self.okul_adi = QLineEdit()

        self.egitim_yili = QComboBox()
        self.egitim_yili.addItems([
            "2026-2027",
            "2027-2028",
            "2028-2029"
        ])

        self.okul_turu = QComboBox()
        self.okul_turu.addItems([
            "Mesleki ve Teknik Anadolu Lisesi"
        ])

        form.addRow("Okul Adı :", self.okul_adi)
        form.addRow("Eğitim Yılı :", self.egitim_yili)
        form.addRow("Okul Türü :", self.okul_turu)

        layout.addLayout(form)

        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.clicked.connect(self.kaydet)

        layout.addWidget(self.btn_kaydet)
        layout.addStretch()

    # ------------------------------------------------------
    # VERİLERİ YÜKLE
    # ------------------------------------------------------

    def verileri_yukle(self):

        okul = okul_getir()

        if okul is None:
            return

        self.okul_adi.setText(okul.okul_adi)

        index = self.egitim_yili.findText(
            okul.egitim_yili
        )

        if index >= 0:
            self.egitim_yili.setCurrentIndex(index)

        index = self.okul_turu.findText(
            okul.okul_turu
        )

        if index >= 0:
            self.okul_turu.setCurrentIndex(index)

    # ------------------------------------------------------
    # KAYDET
    # ------------------------------------------------------

    def kaydet(self):

        okul_adi = self.okul_adi.text().strip()

        if okul_adi == "":

            QMessageBox.warning(
                self,
                "Uyarı",
                "Okul adı boş bırakılamaz."
            )
            return

        okul_kaydet(
            okul_adi,
            self.egitim_yili.currentText(),
            self.okul_turu.currentText()
        )

        QMessageBox.information(
            self,
            "Başarılı",
            "Okul bilgileri kaydedildi."
        )