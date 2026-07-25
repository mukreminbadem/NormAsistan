from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QPushButton,
    QHBoxLayout,
    QHeaderView,
    QTableWidgetItem,
    QMessageBox
)

from database.database import (
    alanlari_getir,
    alan_ekle
)


class AlanlarPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        baslik = QLabel("Alan Bilgileri")
        baslik.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(baslik)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(1)
        self.tablo.setHorizontalHeaderLabels(["Alan Adı"])
        self.tablo.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tablo)

        butonlar = QHBoxLayout()

        self.btnYeni = QPushButton("Yeni Alan")
        self.btnSil = QPushButton("Sil")
        self.btnKaydet = QPushButton("Kaydet")

        butonlar.addWidget(self.btnYeni)
        butonlar.addWidget(self.btnSil)
        butonlar.addStretch()
        butonlar.addWidget(self.btnKaydet)

        layout.addLayout(butonlar)

        self.btnYeni.clicked.connect(self.yeni_satir)
        self.btnKaydet.clicked.connect(self.kaydet)

        self.yukle()

    def yukle(self):

        self.tablo.setRowCount(0)

        for alan in alanlari_getir():

            satir = self.tablo.rowCount()

            self.tablo.insertRow(satir)

            self.tablo.setItem(
                satir,
                0,
                QTableWidgetItem(alan.alan_adi)
            )

    def yeni_satir(self):

        satir = self.tablo.rowCount()

        self.tablo.insertRow(satir)

    def kaydet(self):

        for satir in range(self.tablo.rowCount()):

            hucre = self.tablo.item(satir,0)

            if hucre is None:
                continue

            alan = hucre.text().strip()

            if alan == "":
                continue

            try:
                alan_ekle(alan)
            except:
                pass

        QMessageBox.information(
            self,
            "Bilgi",
            "Alanlar kaydedildi."
        )

        self.yukle()