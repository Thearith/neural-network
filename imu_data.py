from constants import *

class IMUData:

  def __init__(self, accel, gyro, compass, timestamp, is_heel_strike=NON_HEEL_STRIKE):
    self.accel = accel
    self.gyro = gyro
    self.compass = compass
    self.timestamp = timestamp
    self.is_heel_strike = is_heel_strike

  def get_data(self, sensor_type):
    if sensor_type == ACCEL:
      return self.accel
    elif sensor_type == GYRO:
      return self.gyro
    elif sensor_type == COMPASS:
      return self.compass



