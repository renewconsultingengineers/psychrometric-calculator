from PySide6.QtCore import QSize,Qt,QEvent
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QMainWindow, QPushButton, \
    QMessageBox, QTableWidget, QTableView, QTableWidgetItem,QSizePolicy


class PyschroView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Psychrometric Calculator")
        #self.setGeometry(70,50,400,350)
        self.setFixedSize(420,382)           #Window fixed size
        # self.setWindowIcon(QIcon("logo.png")) # window icon

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(10)  # Set vertical spacing between rows
        self.temperature_layout = QHBoxLayout()
        self.rh_layout = QHBoxLayout()
        self.elevation_layout = QHBoxLayout()

        # adding input fields for user to enter temperature
        self.temperature = QLabel("Temperature")
        self.tempInput = QLineEdit()
        #self.tempInput.setPlaceholderText("Please enter dry bulb temperature")
        self.tempInput.setMaximumSize(QSize(60,20))
        self.tempUnit = QLabel("°C")

        #adding widgets to horizontal layout
        self.temperature_layout.addWidget(self.temperature)
        self.temperature_layout.addWidget(self.tempInput)
        self.temperature_layout.addWidget(self.tempUnit)
        self.v_layout.addLayout(self.temperature_layout)

        self.rh = QLabel("Relative Humidity")
        self.rhInput = QLineEdit()
        self.rhInput.setMaximumSize(QSize(60, 20))
        self.rhUnit = QLabel("%")
        self.rh_layout.addWidget(self.rh)
        self.rh_layout.addWidget(self.rhInput)
        self.rh_layout.addWidget(self.rhUnit)
        self.v_layout.addLayout(self.rh_layout)

        self.elevation = QLabel("Elevation")
        self.elevationInput = QLineEdit()
        self.elevationInput.setMaximumSize(QSize(60, 20))
        self.elevationUnit = QLabel("meters")
        self.elevation_layout.addWidget(self.elevation)
        self.elevation_layout.addWidget(self.elevationInput)
        self.elevation_layout.addWidget(self.elevationUnit)
        self.v_layout.addLayout(self.elevation_layout)

        #adding cntral Widget
        widget = QWidget()
        widget.setLayout(self.v_layout)
        self.setCentralWidget(widget)

        self.calculate = QPushButton("Calculate")
        # comment the code if u  dont want to change the button color
        self.calculate.setStyleSheet("""
            QPushButton {
                background-color: #F66107; 
                color: black;   
                font-weight: bold;              
                border: 2px solid gray;     
                border-radius: 5px;         
                padding: 8px;   
                outline:none;
                margin:5px            
            }
            QPushButton:hover {
                background-color: #F66107; 
                color: white;  
                font-weight: bold;                           
            }
           ''' QPushButton:pressed {
                background-color: #E0E0E0;     
                color: white;           
            }'''
        """)
        self.calculate.setFixedWidth(400)
        self.calculate.setDefault(True) # trigger calculate button when clicked on enter key
        self.v_layout.addWidget(self.calculate)

        # Results in tableWidget
        self.table = QTableWidget()
        self.table.setRowCount(6)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Property","Value","Units"])
        #customise table width
        self.table.setColumnWidth(0,200)
        #self.table.resizeColumnsToContents()
        #self.table.horizontalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setStyleSheet("""
                QHeaderView::section {
                    background-color: #F66107; 
                    color: black;             
                    font-weight: bold;       
                    padding: 5px;             
                    border: 1px solid #dcdcdc; 
                }""")                           #FF8000
        self.table.verticalHeader().setVisible(False)  #  row numbers
        self.v_layout.addWidget(self.table)
        # Initialize the table with blank data
        self.initialize_table()

        # Install event filters on input fields
        self.tempInput.installEventFilter(self)
        self.rhInput.installEventFilter(self)
        self.elevationInput.installEventFilter(self)

    def keyPressEvent(self, event):
        # Check if Page Down key is pressed
        if event.key() == Qt.Key.Key_PageDown:
                print(event.key())
                self.focusNextChild()  # Same as Tab navigation
        else:
            super().keyPressEvent(event)

    def displayResult(self,results):
        # Populate the table with results
        for row, (property_name, value, unit) in enumerate(results):

            value_item = QTableWidgetItem(str(value))
            value_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, value_item)

    def initialize_table(self):
        # Fill the table with placeholders
        placeholders = [
            ("Wet Bulb Temperature", "-", "°C"),
            ("Dewpoint Temperature", "-", "°C"),
            ("Absolute Humidity", "-", "g/kg"),
            ("Enthalpy", "-", "kJ/kg"),
            ("Density", "-", "kg/m³"),
            ("Specific heat", "-", "KJ/KgK")
        ]
        for row, (property_name, value, unit) in enumerate(placeholders):
            property_item = QTableWidgetItem(property_name)
            property_item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Disable editing
            property_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, property_item)

            value_item = QTableWidgetItem(value)
            value_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, value_item)

            unit_item = QTableWidgetItem(unit)
            unit_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            unit_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, unit_item)

    def showErrorMessage(self,message):
        QMessageBox.critical(self,"Error",message)

    def inputValidation(self):
        if not self.tempInput.text().strip():
            return False, "Please enter a valid temperature"
        try:
            temperature = float(self.tempInput.text())
            if temperature < -100 or temperature > 100:
                return False, "Temperature must be between -100 and 100"
        except ValueError:
            return False, "Temperature must be a number"

        if not self.rhInput.text():
            return False, "Please enter a valid relative humidity"
        try:
            rh = float(self.rhInput.text())
            if rh < 0 or rh > 100:
                return False, "Relative Humidity must be between 0 and 100%"
        except ValueError:
            return False, "Relative Humidity must be anumber"

        if not self.elevationInput.text():
            return False, "Please enter a valid elevation"
        try:
            elevation = float(self.elevationInput.text())
            if elevation < 0 or elevation > 9000:
                return False,"Elevation must be between 0 and 9000"
        except ValueError:
            return False, "Elevation must be anumber"

        return True, ""









