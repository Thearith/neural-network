from pybrain.tools.customxml     import NetworkReader
from constants                   import *
import file_reader_writer        as file
from feature_extraction          import sync_accel_gyro_compass, extract_peaks, extract_features
from numpy                       import argmax

def normalize(features, max_features, min_features):
  for i in range(len(features)):
    min = min_features[i]
    max = max_features[i]
    if(max == min):
      features[i] = 1
    else:
      features[i] = (features[i] - float(min)) / (float(max) - float(min))

if __name__ == "__main__":

  # get trained network
  fnn = NetworkReader.readFrom(TRAINED_NN_FILE)

  # get data
  for num_file in range(NUM_TEST_FILES):
    file_location = STEP_DETECTION_DATA_LOCATION + "/" + str(num_file+1) + "/"
    accel_list = file.get_sensor_list(file_location + ACCEL_STEP_DETECTION_DATA)
    gyro_list = file.get_sensor_list(file_location + GYRO_STEP_DETECTION_DATA)
    compass_list = file.get_sensor_list(file_location + COMPASS_STEP_DETECTION_DATA)

    imu_list = sync_accel_gyro_compass(accel_list, gyro_list, compass_list)

    # extracting peaks
    accel_y_dict = imu_list.extract_sensor_axis_list(ACCEL, Y_AXIS)
    accel_y = accel_y_dict[READINGS]
    timestamps = accel_y_dict[TIMESTAMPS]

    peaks_index = extract_peaks(accel_y)

    # get normalizer
    max_features = file.get_normalizer(MAX_FEATURE_FILE)
    min_features = file.get_normalizer(MIN_FEATURE_FILE)

    step_count = 0
    index = 0
    # while(index < len(peaks_index)-1):
    start = peaks_index[index]
    for j in range(index+1, len(peaks_index)):
      end = peaks_index[j]

      # extracting features to be input for neural network
      feature = extract_features(imu_list, start, end)
      normalize(feature, max_features, min_features)

      # calculating result
      out = fnn.activate(feature)
      result = out.argmax()
      if(result == HEEL_STRIKE):
        # print start, "\t", end, "\t", out, "\t", result
        start = peaks_index[j]
        index = j
        step_count += 1

    print "File", (num_file+1), "Total step count:", step_count


