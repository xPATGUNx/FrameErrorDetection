from Python.UserInterface import *

# Create the Qt Application
app = QApplication(sys.argv)
# Create and show the form
form = Form()
form.show()
# Run the main Qt loop
sys.exit(app.exec())
