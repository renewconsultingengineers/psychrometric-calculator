from CoolProp.HumidAirProp import HAPropsSI


class PsychroCal:
    def __init__(self, temperature, rh, elevation):
        '''if rh < 0 or rh > 1:
            raise ValueError("Relative Humidity must be between 0 and 100%")
        if temperature < -100 or temperature > 100:
            raise ValueError("Temperature must be between -100 and 100")
        if elevation < 0 or elevation > 9000:
            raise ValueError("Elevation must be between 0 and 9000")'''

        self.temperature = 273.15 + temperature
        self.rh = rh
        self.elevation = elevation

        p0 = 101325  # Sea level standard pressure (Pa)
        l = 0.0065  # Temperature lapse rate (K/m)
        t0 = 288.15  # Standard temperature at sea level (K)
        g = 9.80665  # Gravity (m/s²)
        m = 0.0289644  # Molar mass of air (kg/mol)
        r = 8.31432  # Universal gas constant (J/(mol·K))
        pressure = p0 * (1 - (l * elevation) / t0) ** (g * m / (r * l))
        self.pressure = pressure

    def wet_bulb(self):
        wet_bulb = HAPropsSI("Twb", "T", self.temperature, "RH", self.rh, "P", self.pressure) - 273.15
        return wet_bulb

    def wet_bulb_from_dewpoint(self, dewpoint):
        wet_bulb = HAPropsSI("Twb", "T", self.temperature, "Tdp", (273.15 + dewpoint), "P", self.pressure) - 273.15
        return wet_bulb

    def rh_from_dewpoint(self, dewpoint):
        rh = HAPropsSI("RH", "T", self.temperature, "Tdp", (273.15 + dewpoint), "P", self.pressure)
        return rh

    def absolute_humidity(self):
        absolute_humidity = HAPropsSI("W", "T", self.temperature, "RH", self.rh, "P", self.pressure)
        return absolute_humidity

    def enthalpy(self):
        enthalpy = HAPropsSI("H", "T", self.temperature, "RH", self.rh, "P", self.pressure)
        return enthalpy

    def dewpoint(self):
        dewpoint = HAPropsSI("Tdp", "T", self.temperature, "RH", self.rh, "P", self.pressure) - 273.15
        return dewpoint

    def spec_volume(self):
        spec_volume = HAPropsSI("V", "T", self.temperature, "RH", self.rh, "P", self.pressure)
        density = 1 / spec_volume
        return density

    def specific_heat(self):
        specific_heat = HAPropsSI("C", "T", self.temperature, "RH", self.rh, "P", self.pressure)
        return specific_heat

