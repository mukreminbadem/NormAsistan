from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class BranslarPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        baslik = QLabel("Branş Yönetimi")

        baslik.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(baslik)