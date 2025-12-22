# TidyBit with PySide6 UI

# imports
import sys
from pathlib import Path

from app.utils.helper_function import resource_path
from app.ui.main_window import App
from app.ui.styles import STYLESHEET

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon





# main
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    try:
        icon_path = resource_path("assets/app_logo.png")
        if Path(icon_path).exists():
            app.setWindowIcon(QIcon(icon_path))
    except:
        pass

    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()



