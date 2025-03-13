from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from desktop_app.logic.controller import Controller


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OsBridgeLCCA - Desktop App")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.run_button = QPushButton("Run LCCA Analysis")
        self.run_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_analysis(self):
        """Trigger analysis when button is clicked."""
        controller = Controller()
        controller.run_calculations()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
