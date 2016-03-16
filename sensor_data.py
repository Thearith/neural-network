from vector import Vector

HEEL_STRIKE     = 1
NON_HEEL_STRIKE = 0

ACCEL           = 0
GYRO            = 1
COMPASS         = 2

class SensorData:

  def __init__(self, sensor, timestamp, is_heel_strike=NON_HEEL_STRIKE):
    self.sensor = sensor
    self.timestamp = timestamp
    self.is_heel_strike = is_heel_strike

  def __init__(self, x, y, z, sensor_type, timestamp, is_heel_strike=NON_HEEL_STRIKE):
    self.sensor = Vector(x, y, z, sensor_type)
    self.timestamp = timestamp
    self.is_heel_strike = is_heel_strike