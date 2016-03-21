import imu_data
from constants import *

class IMUList:

  def __init__ (self, list):
    self.imu_list = list
    self.accel_x_list = self.construct_sensor_axis_list(ACCEL, X_AXIS)
    self.accel_y_list = self.construct_sensor_axis_list(ACCEL, Y_AXIS)
    self.accel_z_list = self.construct_sensor_axis_list(ACCEL, Z_AXIS)
    self.gyro_x_list = self.construct_sensor_axis_list(GYRO, X_AXIS)
    self.gyro_y_list = self.construct_sensor_axis_list(GYRO, Y_AXIS)
    self.gyro_z_list = self.construct_sensor_axis_list(GYRO, Z_AXIS)
    self.compass_x_list = self.construct_sensor_axis_list(COMPASS, X_AXIS)
    self.compass_y_list = self.construct_sensor_axis_list(COMPASS, Y_AXIS)
    self.compass_z_list = self.construct_sensor_axis_list(COMPASS, Z_AXIS)


  # public methods

  def extract_sensor_axis_list(self, sensor_type, axis):
    if(sensor_type == ACCEL):
      return self.extract_accel_list(axis)
    elif(sensor_type == GYRO):
      return self.extract_gyro_list(axis)
    else:
      return self.extract_compass_list(axis)


  # private methods

  def construct_sensor_axis_list(self, sensor_type, axis):
    timestamps = []
    readings = []

    for imu in self.imu_list:
      timestamp = imu.timestamp
      reading = imu.get_data(sensor_type).get_reading(axis)
      timestamps.append(timestamp)
      readings.append(reading)

    return {
      TIMESTAMPS: timestamps,
      READINGS: readings
    }

  def extract_accel_list(self, axis):
    if(axis == X_AXIS):
      return self.accel_x_list
    elif(axis == Y_AXIS):
      return self.accel_y_list
    else:
      return self.accel_z_list

  def extract_gyro_list(self, axis):
    if(axis == X_AXIS):
      return self.gyro_x_list
    elif(axis == Y_AXIS):
      return self.gyro_y_list
    else:
      return self.gyro_z_list

  def extract_compass_list(self, axis):
    if(axis == X_AXIS):
      return self.compass_x_list
    elif(axis == Y_AXIS):
      return self.compass_y_list
    else:
      return self.compass_z_list

