from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QFrame,
    QSizePolicy,
)

from ui.okul_page import OkulPage
from ui.alanlar_page import AlanlarPage
from ui.branslar_page import BranslarPage
from ui.subeler_page import SubelerPage
from ui.dersler_page import DerslerPage


class MainWindow(QMainWindow):
    """
    NormAsistan uygulamasının ana penceresi.

    Sol tarafta modül menüsü, sağ tarafta ise seçilen modülün
    içeriği gösterilir.
    """

    def __init__(self):
        super().__init__()

        self.aktif_buton = None
        self.menu_butonlari = []

        self.pencere_ayarlari()
        self.arayuzu_olustur()
        self.sayfalari_olustur()
        self.menu_butonlarini_olustur()

        # Uygulama açıldığında ilk olarak okul bilgileri gösterilir.
        self.sayfa_ac(
            sayfa=self.okul_page,
            buton=self.okul_buton,
        )

    # ======================================================
    # PENCERE AYARLARI
    # ======================================================

    def pencere_ayarlari(self):
        self.setWindowTitle("NormAsistan")

        self.setMinimumSize(
            1100,
            700,
        )

        self.resize(
            1300,
            800,
        )

    # ======================================================
    # ANA ARAYÜZ
    # ======================================================

    def arayuzu_olustur(self):
        self.ana_widget = QWidget()
        self.setCentralWidget(self.ana_widget)

        self.ana_layout = QHBoxLayout(self.ana_widget)
        self.ana_layout.setContentsMargins(0, 0, 0, 0)
        self.ana_layout.setSpacing(0)

        # --------------------------------------------------
        # SOL MENÜ
        # --------------------------------------------------

        self.menu_frame = QFrame()
        self.menu_frame.setObjectName("menuFrame")
        self.menu_frame.setFixedWidth(230)

        self.menu_layout = QVBoxLayout(self.menu_frame)
        self.menu_layout.setContentsMargins(15, 20, 15, 20)
        self.menu_layout.setSpacing(8)

        self.logo_label = QLabel("NormAsistan")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.alt_baslik_label = QLabel(
            "Norm Kadro Yönetim Sistemi"
        )
        self.alt_baslik_label.setObjectName(
            "altBaslikLabel"
        )
        self.alt_baslik_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.alt_baslik_label.setWordWrap(True)

        self.menu_layout.addWidget(self.logo_label)
        self.menu_layout.addWidget(self.alt_baslik_label)

        self.menu_ayirici = QFrame()
        self.menu_ayirici.setFrameShape(
            QFrame.Shape.HLine
        )
        self.menu_ayirici.setObjectName(
            "menuAyirici"
        )

        self.menu_layout.addWidget(self.menu_ayirici)

        # Menü düğmeleri daha sonra oluşturulacak.
        self.menu_buton_layout = QVBoxLayout()
        self.menu_buton_layout.setSpacing(6)

        self.menu_layout.addLayout(
            self.menu_buton_layout
        )

        self.menu_layout.addStretch()

        self.surum_label = QLabel("NormAsistan 2026")
        self.surum_label.setObjectName("surumLabel")
        self.surum_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.menu_layout.addWidget(self.surum_label)

        # --------------------------------------------------
        # SAĞ İÇERİK
        # --------------------------------------------------

        self.icerik_frame = QFrame()
        self.icerik_frame.setObjectName("icerikFrame")

        self.icerik_layout = QVBoxLayout(
            self.icerik_frame
        )
        self.icerik_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.icerik_layout.setSpacing(0)

        self.sayfalar = QStackedWidget()
        self.sayfalar.setObjectName("sayfalar")

        self.icerik_layout.addWidget(self.sayfalar)

        self.ana_layout.addWidget(self.menu_frame)
        self.ana_layout.addWidget(
            self.icerik_frame,
            1,
        )

        self.stilleri_uygula()

    # ======================================================
    # SAYFALAR
    # ======================================================

    def sayfalari_olustur(self):
        """
        Uygulamadaki sayfaları oluşturur ve QStackedWidget
        içerisine ekler.
        """

        self.okul_page = OkulPage()
        self.alanlar_page = AlanlarPage()
        self.branslar_page = BranslarPage()
        self.subeler_page = SubelerPage()
        self.dersler_page = DerslerPage()

        self.sayfalar.addWidget(
            self.okul_page
        )

        self.sayfalar.addWidget(
            self.alanlar_page
        )

        self.sayfalar.addWidget(
            self.branslar_page
        )

        self.sayfalar.addWidget(
            self.subeler_page
        )

        self.sayfalar.addWidget(
            self.dersler_page
        )

    # ======================================================
    # MENÜ DÜĞMELERİ
    # ======================================================

    def menu_butonlarini_olustur(self):
        self.okul_buton = self.menu_butonu_olustur(
            "Okul Bilgileri"
        )

        self.alanlar_buton = self.menu_butonu_olustur(
            "Alanlar"
        )

        self.branslar_buton = self.menu_butonu_olustur(
            "Branşlar"
        )

        self.subeler_buton = self.menu_butonu_olustur(
            "Şubeler"
        )

        self.dersler_buton = self.menu_butonu_olustur(
            "Dersler"
        )

        self.okul_buton.clicked.connect(
            lambda: self.sayfa_ac(
                self.okul_page,
                self.okul_buton,
            )
        )

        self.alanlar_buton.clicked.connect(
            lambda: self.sayfa_ac(
                self.alanlar_page,
                self.alanlar_buton,
            )
        )

        self.branslar_buton.clicked.connect(
            lambda: self.sayfa_ac(
                self.branslar_page,
                self.branslar_buton,
            )
        )

        self.subeler_buton.clicked.connect(
            lambda: self.sayfa_ac(
                self.subeler_page,
                self.subeler_buton,
            )
        )

        self.dersler_buton.clicked.connect(
            lambda: self.sayfa_ac(
                self.dersler_page,
                self.dersler_buton,
            )
        )

    def menu_butonu_olustur(self, metin):
        buton = QPushButton(metin)

        buton.setObjectName("menuButon")
        buton.setCheckable(True)
        buton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        buton.setMinimumHeight(42)

        buton.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.menu_buton_layout.addWidget(buton)
        self.menu_butonlari.append(buton)

        return buton

    # ======================================================
    # SAYFA GEÇİŞİ
    # ======================================================

    def sayfa_ac(self, sayfa, buton):
        """
        Belirtilen sayfayı görüntüler ve ilgili menü düğmesini
        aktif hâle getirir.
        """

        self.sayfalar.setCurrentWidget(sayfa)

        for menu_butonu in self.menu_butonlari:
            menu_butonu.setChecked(
                menu_butonu is buton
            )

        self.aktif_buton = buton

        # Sayfanın yenile metodu varsa sayfa açılırken çalıştırılır.
        yenile_metodu = getattr(
            sayfa,
            "yenile",
            None,
        )

        if callable(yenile_metodu):
            try:
                yenile_metodu()
            except Exception as hata:
                print(
                    f"Sayfa yenilenirken hata oluştu: {hata}"
                )

    # ======================================================
    # STİLLER
    # ======================================================

    def stilleri_uygula(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f3f5f7;
            }

            QFrame#menuFrame {
                background-color: #263445;
                border: none;
            }

            QLabel#logoLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding-top: 5px;
            }

            QLabel#altBaslikLabel {
                color: #cbd3dc;
                font-size: 12px;
                padding-bottom: 10px;
            }

            QFrame#menuAyirici {
                background-color: #455466;
                max-height: 1px;
                border: none;
                margin-top: 5px;
                margin-bottom: 10px;
            }

            QPushButton#menuButon {
                background-color: transparent;
                color: #e9edf2;
                border: none;
                border-radius: 6px;
                padding: 10px 14px;
                text-align: left;
                font-size: 14px;
            }

            QPushButton#menuButon:hover {
                background-color: #34465a;
            }

            QPushButton#menuButon:checked {
                background-color: #1976d2;
                color: white;
                font-weight: bold;
            }

            QLabel#surumLabel {
                color: #9ba8b6;
                font-size: 11px;
                padding-top: 10px;
            }

            QFrame#icerikFrame {
                background-color: #f3f5f7;
                border: none;
            }

            QStackedWidget#sayfalar {
                background-color: #f3f5f7;
                border: none;
            }

            QGroupBox {
                background-color: white;
                border: 1px solid #d8dde3;
                border-radius: 7px;
                margin-top: 12px;
                padding-top: 10px;
                font-weight: bold;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 5px;
                color: #263445;
            }

            QLineEdit,
            QComboBox {
                min-height: 32px;
                border: 1px solid #c7cdd4;
                border-radius: 5px;
                background-color: white;
                padding: 2px 8px;
                font-size: 13px;
            }

            QLineEdit:focus,
            QComboBox:focus {
                border: 1px solid #1976d2;
            }

            QPushButton {
                min-height: 32px;
                padding: 3px 14px;
                border: 1px solid #b8c0c8;
                border-radius: 5px;
                background-color: #ffffff;
                color: #263445;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #edf2f7;
            }

            QPushButton:pressed {
                background-color: #dfe7ef;
            }

            QPushButton:disabled {
                background-color: #eeeeee;
                color: #999999;
                border-color: #d5d5d5;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f8fb;
                border: 1px solid #d8dde3;
                border-radius: 6px;
                gridline-color: #e4e8ec;
                selection-background-color: #d4e8fb;
                selection-color: #1f2933;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QHeaderView::section {
                background-color: #e9eef3;
                color: #263445;
                border: none;
                border-right: 1px solid #d4dae0;
                border-bottom: 1px solid #cbd2d9;
                padding: 7px;
                font-weight: bold;
            }

            QMessageBox {
                background-color: white;
            }
            """
        )