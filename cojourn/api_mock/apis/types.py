from enum import Enum


class DeviceType(str, Enum):
    WATER_HEATER = 'water_heater'
    THERMOSTAT = 'thermostat'
    HOME_BATTERY = 'home_battery'
    EV_CHARGER = 'ev_charger'
    PV_SYSTEM = 'pv_system'
    RAINFOREST_EAGLE = 'power_meter'

class DemandResponseStatus(str, Enum):
    NORMAL = 'normal'
    CURTAILED = 'curtailed'
    HEIGHTENED = 'heightened'
    OPTED_OUT = 'opted_out'

class DeviceStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

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

class WaterHeaterService(str, Enum):
    HIGH_DEMAND = 'high_demand'
    HEAT_PUMP = 'heat_pump'
    NORMAL = 'normal'
    ENERGY_SAVER = 'energy_saver'
    VACATION = 'vacation'

class DeviceService(str, Enum):
    UNLIMITED = 'unlimited'

    HIGH_DEMAND = WaterHeaterService.HIGH_DEMAND
    HEAT_PUMP = WaterHeaterService.HEAT_PUMP
    NORMAL = WaterHeaterService.NORMAL
    ENERGY_SAVER = WaterHeaterService.ENERGY_SAVER
    VACATION = WaterHeaterService.VACATION
