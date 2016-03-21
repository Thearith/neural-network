import sys
from scipy.signal import argrelextrema
from math import sqrt
import file_reader_writer as file
from imu_data import IMUData
from imu_list import IMUList
import sensor_data
from random import shuffle
from constants import *

########################
# CONSTANTS
########################

ACCEL_THRESHOLD = 0.45
TIME_THRESHOLD  = 100



########################################################
# Main function
# Input: a list of accel, gyro, compass sensor data
# Output: a list of features
########################################################

def extract_features_from_data(accel_list, gyro_list, compass_list, ground_truth_list):
  # syncing data
  imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

  accel_y_dict = imu_list.extract_sensor_axis_list(ACCEL, Y_AXIS)
  accel_y = accel_y_dict[READINGS]
  timestamps = accel_y_dict[TIMESTAMPS]

  # extracting features for non heel strike peaks
  peaks_index = extract_peaks(accel_y)
  non_hs_features = extract_feature_list(imu_list, peaks_index, NON_HEEL_STRIKE)

  # extracting features for heel strike
  hs_peaks_index = ground_truth_list
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

def extract_peaks(sensor_list):
  peaks_index = []

  filter_list = []
  filter_list.append(0)
  sample_val = sensor_list[0]
  for i in range(1, len(sensor_list)):
    if(abs(sample_val - sensor_list[i]) >= ACCEL_THRESHOLD):
      sample_val = sensor_list[i]
      filter_list.append(i)

  for i in range(1, len(filter_list)-1):
    prev = filter_list[i-1]
    curr = filter_list[i]
    next = filter_list[i+1]
    if(sensor_list[prev] <= sensor_list[curr] and sensor_list[curr] >= sensor_list[next]):
      peaks_index.append(curr)

  return peaks_index


##############################
# Extracting Features
##############################

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
        features[i][0][j] = (features[i][0][j] - min) / float(max - min)

def extract_feature_list(imu_list, peaks_index, output):
  features = []
  for i in range(len(peaks_index)-1):
    curr_peak_index = peaks_index[i]
    next_peak_index = peaks_index[i+1]
    feature_dict = extract_features(imu_list, curr_peak_index, next_peak_index, output)
    features.append([feature_dict[FEATURES], [feature_dict[OUTPUT]]])
  return features

def extract_features(imu_list, start, end, is_heel_strike):
  accel_features = extract_sensor_features(imu_list, ACCEL, start, end)
  gyro_features = extract_sensor_features(imu_list, GYRO, start, end)
  compass_features = extract_sensor_features(imu_list, COMPASS, start, end)

  features = accel_features + gyro_features + compass_features

  return {
    FEATURES: features,
    OUTPUT: is_heel_strike
  }

def extract_sensor_features(imu_list, sensor_type, start, end):
  x_features = extract_sensor_axis_features(imu_list, sensor_type, X_AXIS, start, end)
  y_features = extract_sensor_axis_features(imu_list, sensor_type, Y_AXIS, start, end)
  z_features = extract_sensor_axis_features(imu_list, sensor_type, Z_AXIS, start, end)

  return x_features + y_features + z_features

def extract_sensor_axis_features(imu_list, sensor_type, axis, start, end):
  sensor_dict = imu_list.extract_sensor_axis_list(sensor_type, axis)
  timestamps = sensor_dict[TIMESTAMPS]
  readings = sensor_dict[READINGS]
  intvl_readings = readings[start:end+1]
  intvl_timestamps = timestamps[start:end+1]


  mean_val = mean(intvl_readings)
  max_val = max(intvl_readings)
  min_val = min(intvl_readings)
  median_val = median(intvl_readings)
  range_val = extract_range(intvl_readings)
  variance_val = variance(intvl_readings)
  std_val = standard_derivation(intvl_readings)

  diff_list = diff(intvl_readings)
  mean_diff_list = mean(diff_list)
  median_diff_list = median(diff_list)
  range_diff_list = extract_range(diff_list)
  std_diff_list = standard_derivation(diff_list)

  peak_to_peak = max_val - min_val
  thres1 = min_val + peak_to_peak * 0.3
  thres2 = min_val + peak_to_peak * 0.5
  thres3 = min_val + peak_to_peak * 0.7
  mean_thres1 = mean(intvl_readings, thres1)
  mean_thres2 = mean(intvl_readings, thres2)
  mean_thres3 = mean(intvl_readings, thres3)

  num_peaks = len(extract_peaks(intvl_readings))
  timestamp = diff_timestamp(intvl_timestamps)

  return [mean_val, max_val, min_val, median_val, range_val, variance_val, std_val,
  mean_diff_list, median_diff_list,
  range_diff_list, std_diff_list, peak_to_peak, mean_thres1, mean_thres2, mean_thres3,
  num_peaks, timestamp]


##########################################################
# Feature Extraction within list, helper functions
##########################################################

def mean(list, threshold=-sys.maxint):
  sum = 0.0
  for val in list:
    if(val >= threshold):
      sum += val

  return sum / float(len(list))

def median(list):
  list.sort()
  half, odd = divmod(len(list), 2)
  if odd:
    return list[half]

  return (list[half - 1] + list[half]) / 2.0

def extract_range(list):
  return max(list) - min(list)

def variance(list):
  mean_val = mean(list)
  sum = 0.0
  for val in list:
    sum += (val - mean_val) * (val - mean_val)

  return sum / float(len(list))

def standard_derivation(list):
  return sqrt(variance(list))

def diff(list):
  diff_list = []
  for i in range(0, len(list)-1):
    diff = list[i+1] -  list[i]
    diff_list.append(diff)

  return diff_list

def diff_timestamp(timestamps):
  return timestamps[-1] - timestamps[0]


if __name__ == "__main__":

  # read file
  file_location = TRAINING_DATA_LOCATION + "/1/"
  accel_list = file.get_sensor_list(file_location + ACCEL_TRAINING_DATA)
  gyro_list = file.get_sensor_list(file_location + GYRO_TRAINING_DATA)
  compass_list = file.get_sensor_list(file_location + COMPASS_TRAINING_DATA)
  ground_truth_list = file.get_ground_truth(file_location + GROUND_TRUTH_DATA)

  features = extract_features_from_data(accel_list, gyro_list, compass_list, ground_truth_list)
  print len(features[0][0])
