import sys

from PySide6.QtWidgets import QApplication

from database.database import veritabani_olustur
from ui.main_window import MainWindow


def main():
    veritabani_olustur()

    uygulama = QApplication(sys.argv)

    pencere = MainWindow()
    pencere.show()

    sys.exit(uygulama.exec())


if __name__ == "__main__":
    main()