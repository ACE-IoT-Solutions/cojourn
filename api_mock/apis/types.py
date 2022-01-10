from enum import Enum

class ThermostatMode(str, Enum):
    AUTO = 'auto'
    HEAT = 'heat'
    COOL = 'cool'
    ECO  = 'eco'
    OFF  = 'off'

class Weather(str, Enum):
    CLEAR = 'clear'
    CLOUDY = 'cloudy'
    PARTLY_CLOUDY = 'partly_cloudy'
    RAINY = 'rainy'
    WINDY = 'windy'

class ChargeRate(str, Enum):
    IDLE = 'idle'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class ChargeService(str, Enum):
    UNLIMITED = 'unlimited'
