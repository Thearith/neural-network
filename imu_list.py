import imu_data

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
