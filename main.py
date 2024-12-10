from PyQt5.QtWidgets import QApplication
import database
from database import db_manager
from static.ui.main_window import MainWindow
from  database.models import  Models

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    models = Models(db_manager)

    main_window = MainWindow(models)
    main_window.show()

    sys.exit(app.exec())
