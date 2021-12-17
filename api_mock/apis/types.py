from enum import Enum

class ThermostatMode(Enum):
    AUTO = 'auto'
    HEAT = 'heat'
    COOL = 'cool'
    ECO  = 'eco'
    OFF  = 'off'

class Weather(Enum):
    CLEAR = 'clear'
    CLOUDY = 'cloudy'
    PARTLY_CLOUDY = 'partly_cloudy'
    RAINY = 'rainy'
    WINDY = 'windy'
