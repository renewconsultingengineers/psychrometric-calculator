from model.psychro_model import *

class PsychroController:
    def __init__(self, view):
        self.view = view

        # Upon clicking Calculate btn,perform logics which is done in model class
        self.view.calculate.clicked.connect(self.calculate_psychro)
        self.view.tempInput.returnPressed.connect(self.calculate_psychro)
        self.view.rhInput.returnPressed.connect(self.calculate_psychro)
        self.view.elevationInput.returnPressed.connect(self.calculate_psychro)

    def calculate_psychro(self):
        is_valid, error_message = self.view.inputValidation()
        if not is_valid:
            self.view.showErrorMessage(error_message)
            return

        # Getting data/inputs from the View
        temperature = float(self.view.tempInput.text())
        rh = float(self.view.rhInput.text()) / 100
        elevation = float(self.view.elevationInput.text())

        #  calculations using model class
        point = PsychroCal(temperature, rh, elevation)
        Twb = round(PsychroCal.wet_bulb(point), 2)
        Tdp = round(PsychroCal.dewpoint(point), 2)
        W = PsychroCal.absolute_humidity(point)
        H = PsychroCal.enthalpy(point)
        C = round(PsychroCal.specific_heat(point) / 1000, 2)
        absolute_humidity = round(W*1000, 2)
        enthalpy = round(H/1000,2)
        density = round(PsychroCal.spec_volume(point), 2)
        Twb_from_Tdp = PsychroCal.wet_bulb_from_dewpoint(point, Tdp)
        rh_from_Tdp = PsychroCal.rh_from_dewpoint(point, Tdp)

        results = [                             # results string
            ("Wet Bulb Temperature",Twb,"°C"),
            ("Dewpoint Temperature", Tdp,"°C"),
            ("Absolute Humidity", absolute_humidity, "g/kg"),
            ("Enthalpy", enthalpy, "kJ/kg"),
            ("Density", density, "kg/m³"),
            ("Specific heat", C, "KJ/KgK")

        ]
        # Display results in the QTableWidget
        self.view.displayResult(results)


