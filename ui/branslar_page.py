from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)

from database.database import (
    branslari_getir,
    brans_ekle,
    brans_sil
)


class BranslarPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # ======================================
        # Başlık
        # ======================================

        baslik = QLabel("Branş Yönetimi")
        baslik.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            padding:8px;
        """)

        layout.addWidget(baslik)

        # ======================================
        # Üst Alan
        # ======================================

        ust = QHBoxLayout()

        self.txtMebKodu = QLineEdit()
        self.txtMebKodu.setPlaceholderText("MEB Kodu")

        self.txtBrans = QLineEdit()
        self.txtBrans.setPlaceholderText("Branş Adı")

        self.btnEkle = QPushButton("Ekle")

        ust.addWidget(self.txtMebKodu)
        ust.addWidget(self.txtBrans)
        ust.addWidget(self.btnEkle)

        layout.addLayout(ust)

        # ======================================
        # Tablo
        # ======================================

        self.tablo = QTableWidget()

        self.tablo.setColumnCount(3)

        self.tablo.setHorizontalHeaderLabels([
            "ID",
            "MEB Kodu",
            "Branş Adı"
        ])

        self.tablo.verticalHeader().setVisible(False)

        self.tablo.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.tablo.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.tablo.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tablo.setAlternatingRowColors(True)

        header = self.tablo.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        layout.addWidget(self.tablo)

        # ======================================
        # Alt Butonlar
        # ======================================

        alt = QHBoxLayout()

        self.btnSil = QPushButton("Sil")

        alt.addStretch()
        alt.addWidget(self.btnSil)

        layout.addLayout(alt)

        # ======================================
        # Bilgi
        # ======================================

        self.lblToplam = QLabel()

        self.lblToplam.setAlignment(Qt.AlignRight)

        layout.addWidget(self.lblToplam)

        # ======================================
        # Olaylar
        # ======================================

        self.btnEkle.clicked.connect(self.ekle)
        self.btnSil.clicked.connect(self.sil)

        self.txtBrans.returnPressed.connect(self.ekle)
        self.txtMebKodu.returnPressed.connect(self.ekle)

        self.listele()

    # ===================================================

    def listele(self):

        self.tablo.setRowCount(0)

        branslar = branslari_getir()

        for brans in branslar:

            satir = self.tablo.rowCount()

            self.tablo.insertRow(satir)

            self.tablo.setItem(
                satir,
                0,
                QTableWidgetItem(str(brans.id))
            )

            self.tablo.setItem(
                satir,
                1,
                QTableWidgetItem(brans.meb_kodu or "")
            )

            self.tablo.setItem(
                satir,
                2,
                QTableWidgetItem(brans.brans_adi)
            )

        self.lblToplam.setText(
            f"Toplam Branş : {len(branslar)}"
        )

    # ===================================================

    def ekle(self):

        meb = self.txtMebKodu.text().strip()
        ad = self.txtBrans.text().strip()

        if ad == "":

            QMessageBox.warning(
                self,
                "Uyarı",
                "Branş adı boş bırakılamaz."
            )
            return

        sonuc = brans_ekle(ad, meb)

        if sonuc:

            self.txtMebKodu.clear()
            self.txtBrans.clear()

            self.txtMebKodu.setFocus()

            self.listele()

        else:

            QMessageBox.information(
                self,
                "Bilgi",
                "Bu branş zaten kayıtlı."
            )

    # ===================================================

    def sil(self):

        satir = self.tablo.currentRow()

        if satir < 0:

            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen silinecek branşı seçiniz."
            )
            return

        brans_id = int(
            self.tablo.item(satir, 0).text()
        )

        cevap = QMessageBox.question(
            self,
            "Sil",
            "Seçilen branş silinsin mi?"
        )

        if cevap == QMessageBox.Yes:

            brans_sil(brans_id)

            self.listele()