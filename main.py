from PySide2.QtWidgets import QApplication, QMessageBox
from ui import Stats

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
