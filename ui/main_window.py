from PySide6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QStackedWidget,
    QWidget,
    QHBoxLayout,
    QStatusBar
)

from ui.okul_page import OkulPage
from ui.alanlar_page import AlanlarPage
from ui.subeler_page import SubelerPage
from ui.branslar_page import BranslarPage

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NormAsistan 2026")
        self.resize(1400, 850)

        # Ana Widget
        merkez = QWidget()
        self.setCentralWidget(merkez)

        layout = QHBoxLayout()
        merkez.setLayout(layout)

        #################################################
        # SOL MENÜ
        #################################################

        self.menu = QListWidget()

        self.menu.addItems([
            "🏫 Okul Bilgileri",
            "📚 Alanlar",
            "👨‍🏫 Branşlar",
            "👥 Şubeler",
            "📅 Ders Çizelgeleri",
            "➗ Grup Sayıları",
            "📖 Seçmeli Dersler",
            "🧮 Ders Yükü",
            "👨‍🏫 Norm Kadro",
            "📊 Raporlar"
        ])

        self.menu.setMaximumWidth(260)

        layout.addWidget(self.menu)

        #################################################
        # SAYFALAR
        #################################################

        self.sayfalar = QStackedWidget()

        layout.addWidget(self.sayfalar)

        #################################################
        # GERÇEK SAYFALAR
        #################################################

        self.okul = OkulPage()
        self.alanlar = AlanlarPage()
        self.branslar = BranslarPage()
        self.subeler = SubelerPage()

        self.sayfalar.addWidget(self.okul)
        self.sayfalar.addWidget(self.alanlar)
        self.sayfalar.addWidget(self.branslar)
        self.sayfalar.addWidget(self.subeler)

        #################################################
        # ŞİMDİLİK BOŞ SAYFALAR
        #################################################

        self.ders_cizelgeleri = QWidget()
        self.grup_sayilari = QWidget()
        self.secmeli_dersler = QWidget()
        self.ders_yuku = QWidget()
        self.norm_kadro = QWidget()
        self.raporlar = QWidget()

        self.sayfalar.addWidget(self.ders_cizelgeleri)
        self.sayfalar.addWidget(self.grup_sayilari)
        self.sayfalar.addWidget(self.secmeli_dersler)
        self.sayfalar.addWidget(self.ders_yuku)
        self.sayfalar.addWidget(self.norm_kadro)
        self.sayfalar.addWidget(self.raporlar)

        #################################################
        # MENÜ
        #################################################

        self.menu.currentRowChanged.connect(self.sayfa_degistir)

        self.menu.setCurrentRow(0)

        #################################################
        # STATUS BAR
        #################################################

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Hazır")

    def sayfa_degistir(self, index):
        self.sayfalar.setCurrentIndex(index)