import sys

from PySide6.QtWidgets import QApplication
from controller.psychro_controller import PsychroController
from view.psychro_view import PyschroView

if __name__ == "__main__":
    app = QApplication([])
    view = PyschroView()     # adding view
    controller = PsychroController(view) # adding controller
    view.show()        # show my View
    sys.exit(app.exec())

