from vector import Vector
from constants import *

class SensorData:

  def __init__(self, sensor, timestamp, is_heel_strike=NON_HEEL_STRIKE):
    self.sensor = sensor
    self.timestamp = timestamp
    self.is_heel_strike = is_heel_strike

  def __init__(self, x, y, z, sensor_type, timestamp, is_heel_strike=NON_HEEL_STRIKE):
    self.sensor = Vector(x, y, z, sensor_type)
    self.timestamp = timestamp
    self.is_heel_strike = is_heel_strike