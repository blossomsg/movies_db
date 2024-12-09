from PySide2.QtWidgets import QApplication

from movies_db_sql_ui import CSVWin

if __name__ == "__main__":
    app = QApplication([])
    win = CSVWin()
    win.show()
    app.exec_()
