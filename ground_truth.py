import sys
import file_reader_writer as file
from imu_data import IMUData
from imu_list import IMUList
from constants import *


########################
# CONSTANTS
########################

ACCEL_THRESHOLD = 0.45
TIME_THRESHOLD  = 250
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


def extract_heel_strike_peaks(timestamps, accel_list, peaks_index, ground_truth_list):
  hs_peaks_index = []
  index = -1

  for timestamp in ground_truth_list:
    closest_index = peaks_index[0]
    min_diff = sys.maxint
    closest = []

    for j in range(index+1, len(peaks_index)):
      peak_index = peaks_index[j]
      diff = abs(timestamp - timestamps[peak_index] - LAG_TIME)
      if min_diff > diff:
        min_diff = diff
        closest_index = peak_index
      if diff < TIME_THRESHOLD:
        closest.append(peak_index)

    if(len(closest) > 1):
      highest_peak_index = closest[0]
      highest_peak_val = -sys.maxint
      for i in closest:
        if highest_peak_val < accel_list[i]:
          highest_peak_val = accel_list[i]
          highest_peak_index = i
      closest_index = highest_peak_index

    index = peaks_index.index(closest_index)
    hs_peaks_index.append(closest_index)

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
    if(sensor_list[prev] < sensor_list[curr] and sensor_list[curr] > sensor_list[next]):
      peaks_index.append(curr)

  return peaks_index


if __name__ == "__main__":

  for num_file in range(1, NUM_RAW_FILES):

    print "Currently in file:", (num_file+1)

    file_location = TRAINING_DATA_LOCATION + "/" + str(num_file+1) + "/"
    accel_list = file.get_sensor_list(file_location + ACCEL_TRAINING_DATA)
    gyro_list = file.get_sensor_list(file_location + GYRO_TRAINING_DATA)
    compass_list = file.get_sensor_list(file_location + COMPASS_TRAINING_DATA)
    ground_truth_list = file.get_ground_truth_raw(file_location + GROUND_TRUTH_DATA_RAW)

    imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

    accel_y_dict = imu_list.extract_sensor_axis_list(ACCEL, Y_AXIS)
    accel_y = accel_y_dict[READINGS]
    timestamps = accel_y_dict[TIMESTAMPS]
    peaks_index = extract_peaks(accel_y)

    heel_strikes = extract_heel_strike_peaks(timestamps, accel_y, peaks_index, ground_truth_list)

    # write to file
    outputs = []
    for heel_strike in heel_strikes:
      outputs.append(str(heel_strike))
    file.write_file(file_location + GROUND_TRUTH_DATA, outputs)


