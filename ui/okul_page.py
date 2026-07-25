from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QLabel
)


class OkulPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        baslik = QLabel("Okul Bilgileri")
        baslik.setStyleSheet("font-size:22px;font-weight:bold;")

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

        self.btn = QPushButton("Kaydet")

        layout.addWidget(self.btn)
        layout.addStretch()