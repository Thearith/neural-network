import numpy as np
from scipy.signal import argrelextrema
import math
import file_reader_writer as file
from imu_data import IMUData
from imu_list import IMUList
import sensor_data

ACCEL_TRAINING_DATA   = "training/March 14 2016 - 19-17-55-698 - Accel.txt"
GYRO_TRAINING_DATA    = "training/March 14 2016 _ 19_17_55_698 - Gyro.txt"
COMPASS_TRAINING_DATA = "training/March 14 2016 _ 19_17_55_698 - Compass.txt"

TROUGHS       = "troughs"
PEAKS         = "peaks"

INPUT         = "features"
OUTPUT        = "output"

ACCEL_THRESHOLD = 1


##############################
# Syncing Datas
##############################

def sync_accel_gyro_compass(accel_list, gyro_list, compass_list):
  min_size = min([len(accel_list), len(gyro_list), len(compass_list)])

  accel_list = accel_list[:min_size]
  gyro_list = gyro_list[:min_size]
  compass_list = compass_list[:min_size]

  imu_list = []

  for i in range(min_size):
    accel = accel_list[i]
    gyro = gyro_list[i]
    compass = compass_list[i]
    if(accel.timestamp == gyro.timestamp == compass.timestamp):
      imu_data = IMUData(accel.sensor, gyro.sensor, compass.sensor, accel.timestamp, accel.is_heel_strike)
      imu_list.append(imu_data)

  return IMUList(imu_list)


#########################################
# Peaks and Troughs Detection
#########################################

def extract_peaks_troughs(sensor_dict):
  peaks_timestamp = []
  troughs_timestamp = []

  timestamp = sensor_dict.keys()
  sensor_data = sensor_dict.values()

  filter_list = []
  filter_list.append(0)
  sample_val = sensor_data[0]
  for i in range(1, len(sensor_data)):
    if(abs(sample_val - sensor_data[i]) <= ACCEL_THRESHOLD):
      sample_val = sensor_data[i]
      filter_list.append(i)

  for i in range(1, len(filter_list)-1):
    prev = filter_list[i-1]
    curr = filter_list[i]
    next = filter_list[i+1]
    if(sensor_data[prev] <= sensor_data[curr] and sensor_data[curr] >= sensor_data[next]):
      peaks_timestamp.append(timestamp[curr])
    if(sensor_data[prev] >= sensor_data[curr] and sensor_data[curr] <= sensor_data[next]):
      troughs_timestamp.append(timestamp[curr])

  return {
    PEAKS: peaks_timestamp,
    TROUGHS: troughs_timestamp
  }


##############################
# Extracting Features
##############################

def extract_features(imu_list, start, end):
  accel_features = extract_sensor_features(imu_list, sensor_data.ACCEL, start, end)
  gyro_features = extract_sensor_features(imu_list, sensor_data.GYRO, start, end)
  compass_features = extract_sensor_features(imu_list, sensor_data.COMPASS, start, end)

  return accel_features + gyro_features + compass_features

def extract_sensor_features(imu_list, sensor_type, start, end):
  x_features = extract_sensor_axis_features(imu_list, sensor_type, sensor_data.X_AXIS, start, end)
  y_features = extract_sensor_axis_features(imu_list, sensor_type, sensor_data.Y_AXIS, start, end)
  z_features = extract_sensor_axis_features(imu_list, sensor_type, sensor_data.Z_AXIS, start, end)

  return x_features + y_features + z_features

def extract_sensor_axis_features(imu_list, sensor_type, axis, start, end):
  sensor_dict = imu_list.extract_sensor_axis_list(sensor_type, axis)
  timestamp = sensor_dict.keys()
  datas = sensor_dict.values()


def mean(list, start, end):
  if(start > end):
    return mean(list, end, start)

  sum = 0.0
  for i in range(start, end+1):
    sum += list[i]

  return sum / (end - start + 1)


def median(list, start, end):
  if(start > end):
    return median(list, end, start)

  array = list[start:end+1]
  array = sort(array)
  half, odd = divmod(len(array), 2)
  if odd:
    return array[half]

  return (array[half - 1] + array[half]) / 2.0


def mode(list, start, end):
  if(start > end):
    return mode(list, end, start)

  count = {}
  for i in range(start, end+1):
    if list[i] in count.keys():
      count[list[i]] += 1
    else:
      count[list[i]] = 1

  highestNum = 0
  for i in count.keys():
    if(count[i] > highestNum):
      highestNum = count[i]
      mode = i

  if(highestNum == 1):
    return mean(list, start, end)

  return mode


def diff(list, start, end):
  if(start > end):
    return diff(list, end, start)

  return max(list) - min(list)


def variance(list, start, end):
  if(start > end):
    return variance(list, end, start)

  mean = mean(list, start, end)
  sum = 0.0
  for i in range(start, end+1):
    sum += (list[i] - mean) * (list[i] - mean)

  return sum / (end - start + 1)


def standard_derivation(list, start, end):
  if(start > end):
    return standard_derivation(list, end, start)

  return math.sqrt(variance(list, start, end))


if __name__ == "__main__":

  # getting sensor list and trim data
  accel_list = file.get_sensor_list(ACCEL_TRAINING_DATA)
  gyro_list = file.get_sensor_list(GYRO_TRAINING_DATA)
  compass_list = file.get_sensor_list(COMPASS_TRAINING_DATA)

  imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

  # finding peaks and troughs
  accel_y = imu_list.extract_sensor_axis_list(sensor_data.ACCEL, sensor_data.X_AXIS)
  peaks_and_troughs = extract_peaks_troughs(accel_y)
  print len(peaks_and_troughs[PEAK]), len(peaks_and_troughs[TROUGHS  ])

