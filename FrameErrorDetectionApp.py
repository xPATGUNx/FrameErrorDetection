import sys
from Python.UserInterface import *

app = QApplication(sys.argv)
ui = UserInterface()
ui.show()
sys.exit(app.exec())
