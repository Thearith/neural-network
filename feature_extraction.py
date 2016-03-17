import sys
from scipy.signal import argrelextrema
from math import sqrt
import file_reader_writer as file
from imu_data import IMUData
from imu_list import IMUList
import sensor_data
from random import shuffle

ACCEL_TRAINING_DATA   = "training/March 14 2016 - 19-17-55-698 - Accel.txt"
GYRO_TRAINING_DATA    = "training/March 14 2016 _ 19_17_55_698 - Gyro.txt"
COMPASS_TRAINING_DATA = "training/March 14 2016 _ 19_17_55_698 - Compass.txt"

FEATURES      = "features"
OUTPUT        = "output"

HEEL_STRIKE     = 1
NON_HEEL_STRIKE = 0

ACCEL_THRESHOLD = 1


########################################################
# Main function
# Input: a list of accel, gyro, compass sensor data
# Output: a list of features
########################################################

def extract_features_from_data(accel_list, gyro_list, compass_list):
  # syncing data
  imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

  accel_y = imu_list.extract_sensor_axis_list(sensor_data.ACCEL, sensor_data.Y_AXIS)
  heel_strike = imu_list.extract_heel_strikes()

  # extracting features for non heel strike peaks
  non_hs_peaks_index = extract_peaks(accel_y)
  non_hs_features = extract_feature_list(imu_list, non_hs_peaks_index, NON_HEEL_STRIKE)

  # extracting features for heel strike
  hs_peaks_index = extract_heel_strike_peaks(heel_strike)
  hs_features = extract_feature_list(imu_list, hs_peaks_index, HEEL_STRIKE)

  # combining the features
  features = non_hs_features + hs_features
  normalize(features)
  shuffle(features)

  return features


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
# Local Maximas Detection
#########################################

def extract_peaks(sensor_dict):
  peaks_index = []

  sensor_list = sensor_dict.values()

  filter_list = []
  filter_list.append(0)
  sample_val = sensor_list[0]
  for i in range(1, len(sensor_list)):
    if(abs(sample_val - sensor_list[i]) <= ACCEL_THRESHOLD):
      sample_val = sensor_list[i]
      filter_list.append(i)

  for i in range(1, len(filter_list)-1):
    prev = filter_list[i-1]
    curr = filter_list[i]
    next = filter_list[i+1]
    if(sensor_list[prev] <= sensor_list[curr] and sensor_list[curr] >= sensor_list[next]):
      peaks_index.append(curr)

  return peaks_index

def extract_heel_strike_peaks(heel_strike_dict):
  peaks_index = []
  heel_strikes_list = heel_strike_dict.values()

  for i in range(len(heel_strikes_list)):
    if(heel_strikes_list[i] == HEEL_STRIKE):
      peaks_index.append(i)

  return peaks_index


##############################
# Extracting Features
##############################

def extract_feature_list(imu_list, peaks_index, output):
  features = []
  for i in range(len(peaks_index)-1):
    curr_peak_index = peaks_index[i]
    next_peak_index = peaks_index[i+1]
    feature_dict = extract_features(imu_list, curr_peak_index, next_peak_index, output)
    features.append([feature_dict[FEATURES], [feature_dict[OUTPUT]]])
  return features

def extract_features(imu_list, start, end, is_heel_strike):
  accel_features = extract_sensor_features(imu_list, sensor_data.ACCEL, start, end)
  gyro_features = extract_sensor_features(imu_list, sensor_data.GYRO, start, end)
  compass_features = extract_sensor_features(imu_list, sensor_data.COMPASS, start, end)

  features = accel_features + gyro_features + compass_features

  return {
    FEATURES: features,
    OUTPUT: is_heel_strike
  }

def extract_sensor_features(imu_list, sensor_type, start, end):
  x_features = extract_sensor_axis_features(imu_list, sensor_type, sensor_data.X_AXIS, start, end)
  y_features = extract_sensor_axis_features(imu_list, sensor_type, sensor_data.Y_AXIS, start, end)
  z_features = extract_sensor_axis_features(imu_list, sensor_type, sensor_data.Z_AXIS, start, end)

  return x_features + y_features + z_features

def extract_sensor_axis_features(imu_list, sensor_type, axis, start, end):
  sensor_dict = imu_list.extract_sensor_axis_list(sensor_type, axis)
  timestamp = sensor_dict.keys()
  datas = sensor_dict.values()

  mean_val = mean(datas, start, end)
  median_val = median(datas, start, end)
  mode_val = mode(datas, start, end)
  diff_val = mode(datas, start, end)
  variance_val = variance(datas, start, end)
  standard_derivation_val = standard_derivation(datas, start, end)

  return [mean_val, median_val, mode_val, diff_val, variance_val, standard_derivation_val]


def normalize(features):
  features_len = len(features[0][0])
  max_features = [-sys.maxint for i in range(features_len)]
  min_features = [sys.maxint for i in range(features_len)]

  for i in range(len(features)):
    for j in range(len(features[i][0])):
      if(max_features[j] < features[i][0][j]):
        max_features[j] = features[i][0][j]
      if(min_features[j] > features[i][0][j]):
        min_features[j] = features[i][0][j]

  # normalize
  for i in range(len(features)):
    for j in range(len(features[i][0])):
      min = min_features[j]
      max = max_features[j]
      if(max == min):
        features[i][0][j] = 1
      else:
        features[i][0][j] = (features[i][0][j] - min) / (float)(max - min)


##########################################################
# Feature Extraction within list, helper functions
##########################################################

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
  array.sort()
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

  mean_val = mean(list, start, end)
  sum = 0.0
  for i in range(start, end+1):
    sum += (list[i] - mean_val) * (list[i] - mean_val)

  return sum / (end - start + 1)


def standard_derivation(list, start, end):
  if(start > end):
    return standard_derivation(list, end, start)

  return sqrt(variance(list, start, end))


if __name__ == "__main__":

  # getting sensor list and trim data
  accel_list = file.get_sensor_list(ACCEL_TRAINING_DATA)
  gyro_list = file.get_sensor_list(GYRO_TRAINING_DATA)
  compass_list = file.get_sensor_list(COMPASS_TRAINING_DATA)

  features = extract_features_from_data(accel_list, gyro_list, compass_list)
  print features[0], len(features[0][0])
