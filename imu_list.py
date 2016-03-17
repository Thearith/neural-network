import imu_data

HEEL_STRIKE     = 1
NON_HEEL_STRIKE = 0

ACCEL           = 0
GYRO            = 1
COMPASS         = 2

X_AXIS  = 0
Y_AXIS  = 1
Z_AXIS  = 2

class IMUList:
  def __init__ (self, list):
    self.imu_list = list

  def extract_sensor_list(self, sensor_type):
    dict = {}
    for imu in self.imu_list:
      dict[imu.timestamp] = imu.get_data(sensor_type)

    return dict

  def extract_sensor_axis_list(self, sensor_type, axis):
    dict = {}
    for imu in self.imu_list:
        dict[imu.timestamp] = imu.get_data(sensor_type).get_reading(axis)

    return dict

  def extract_heel_strikes(self):
    dict = {}
    for imu in self.imu_list:
        dict[imu.timestamp] = imu.is_heel_strike

    return dict

  def is_heel_strike(self, index):
    return self.imu_list[index].is_heel_strike == HEEL_STRIKE
