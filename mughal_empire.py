import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MughalEmpireApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Mughal Empire - Virtual Museum")
        self.setGeometry(100, 100, 1200, 800)

        # Set the main widget (central widget)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://sketchfab.com/models/d81410fe83f54c45b0caffe9490cf5d3/embed"))
        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        
        # Create a widget to hold the layout and set as central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Customize the background color
        self.setStyleSheet("background-color: #8B4513;")  # Brown color

        # Show the window
        self.show()

# Create and run the application
app = QApplication(sys.argv)
window = MughalEmpireApp()
sys.exit(app.exec_())
