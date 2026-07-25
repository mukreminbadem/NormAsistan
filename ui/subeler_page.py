from database.database import alanlari_getir

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
    QHBoxLayout,
    QHeaderView,
    QComboBox,
    QSpinBox,
    QMessageBox
)


class SubelerPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        baslik = QLabel("Şube Bilgileri")
        baslik.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(baslik)

        self.tablo = QTableWidget()

        self.tablo.setColumnCount(4)

        self.tablo.setHorizontalHeaderLabels([
            "Sınıf",
            "Alan",
            "Şube",
            "Öğrenci Sayısı"
        ])

        self.tablo.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tablo)

        butonlar = QHBoxLayout()

        self.btnYeni = QPushButton("Yeni Şube")
        self.btnSil = QPushButton("Seçili Satırı Sil")
        self.btnKaydet = QPushButton("Kaydet")

        butonlar.addWidget(self.btnYeni)
        butonlar.addWidget(self.btnSil)
        butonlar.addStretch()
        butonlar.addWidget(self.btnKaydet)

        layout.addLayout(butonlar)

        self.btnYeni.clicked.connect(self.yeni_sube)
        self.btnSil.clicked.connect(self.satir_sil)

        self.yeni_sube()

    def yeni_sube(self):

        satir = self.tablo.rowCount()

        self.tablo.insertRow(satir)

        ##################################
        # SINIF
        ##################################

        sinif = QComboBox()
        sinif.addItems(["9", "10", "11", "12"])

        ##################################
        # ALAN
        ##################################

        alan = QComboBox()

        alanlar = alanlari_getir()

        if alanlar:

            for kayit in alanlar:
                alan.addItem(kayit.alan_adi)

        else:

            alan.addItem("Alan tanımlanmamış")

        ##################################
        # ŞUBE
        ##################################

        sube = QComboBox()

        sube.addItems([
            "A","B","C","D","E","F","G","H",
            "I","J","K","L","M","N","O","P",
            "R","S","T","U","V","Y","Z"
        ])

        ##################################
        # ÖĞRENCİ SAYISI
        ##################################

        ogrenci = QSpinBox()

        ogrenci.setRange(0,50)

        ogrenci.setValue(24)

        ##################################
        # TABLO
        ##################################

        self.tablo.setCellWidget(satir,0,sinif)
        self.tablo.setCellWidget(satir,1,alan)
        self.tablo.setCellWidget(satir,2,sube)
        self.tablo.setCellWidget(satir,3,ogrenci)

    def satir_sil(self):

        satir = self.tablo.currentRow()

        if satir == -1:

            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen silmek istediğiniz satırı seçiniz."
            )

            return

        self.tablo.removeRow(satir)