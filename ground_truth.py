import sys
import file_reader_writer as file
from imu_data import IMUData
from imu_list import IMUList
from constants import *


########################
# CONSTANTS
########################

ACCEL_THRESHOLD = 0.45
TIME_THRESHOLD  = 100
LAG_TIME        = 100


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


def extract_heel_strike_peaks(timestamps, peaks_index, ground_truth_list):
  hs_peaks_index = []

  for timestamp in ground_truth_list:
    closest_index = peaks_index[0]
    min_diff = sys.maxint
    for peak_index in peaks_index:
      diff = abs(timestamp - timestamps[peak_index] - LAG_TIME)
      if min_diff > diff:
        min_diff = diff
        closest_index = peak_index
    print closest_index, min_diff
    hs_peaks_index.append([closest_index, min_diff])

  return hs_peaks_index

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


if __name__ == "__main__":
  file_location = TRAINING_DATA_LOCATION + "/1/"
  accel_list = file.get_sensor_list(file_location + ACCEL_TRAINING_DATA)
  gyro_list = file.get_sensor_list(file_location + GYRO_TRAINING_DATA)
  compass_list = file.get_sensor_list(file_location + COMPASS_TRAINING_DATA)
  ground_truth_list = file.get_ground_truth_raw(file_location + GROUND_TRUTH_DATA_RAW)

  imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

  accel_y_dict = imu_list.extract_sensor_axis_list(ACCEL, Y_AXIS)
  accel_y = accel_y_dict[READINGS]
  timestamps = accel_y_dict[TIMESTAMPS]
  peaks_index = extract_peaks(accel_y)

  heel_strikes = extract_heel_strike_peaks(timestamps, peaks_index, ground_truth_list)

  # write to file
  outputs = []
  for heel_strike in heel_strikes:
    output = str(heel_strike[0]) + "\t" + str(heel_strike[1])
    outputs.append(output)
  file.write_file(file_location + GROUND_TRUTH_DATA, outputs)


