from pybrain.tools.customxml     import NetworkReader
from constants                   import *
import file_reader_writer        as file
from feature_extraction          import sync_accel_gyro_compass, extract_peaks, extract_features

if __name__ == "__main__":
  # get trained network
  fnn = NetworkReader.readFrom(TRAINED_NN_FILE)

  # get data
  file_location = STEP_DETECTION_DATA_LOCATION + "/"
  accel_list = file.get_sensor_list(file_location + ACCEL_STEP_DETECTION_DATA)
  gyro_list = file.get_sensor_list(file_location + GYRO_STEP_DETECTION_DATA)
  compass_list = file.get_sensor_list(file_location + COMPASS_STEP_DETECTION_DATA)

  imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

  accel_y_dict = imu_list.extract_sensor_axis_list(ACCEL, Y_AXIS)
  accel_y = accel_y_dict[READINGS]
  timestamps = accel_y_dict[TIMESTAMPS]

  peaks_index = extract_peaks(accel_y)

  step_count = 0
  index = 0
  # while(index < len(peaks_index)-1):
  start = peaks_index[index]
  for j in range(index+1, len(peaks_index)):
    end = peaks_index[j]
    feature = extract_features(imu_list, start, end)
    result = fnn.activate(feature)
    print index, j, result


