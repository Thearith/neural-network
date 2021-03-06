# feature extraction
HEEL_STRIKE             = 1
NON_HEEL_STRIKE         = 0

ACCEL                   = 0
GYRO                    = 1
COMPASS                 = 2

X_AXIS                  = 0
Y_AXIS                  = 1
Z_AXIS                  = 2

TIMESTAMPS              = "timestamps"
READINGS                = "readings"
HEEL_STRIKES            = "heel_strikes"

FEATURES                = "features"
OUTPUT                  = "output"

MAX                     = "maximum"
MIN                     = "minimum"


# training
NUM_RAW_FILES           = 6
TRAINING_DATA_LOCATION  = "training"
DEBUG_TRAINING_DATA     = "debug"
ACCEL_TRAINING_DATA     = "Accel.txt"
GYRO_TRAINING_DATA      = "Gyro.txt"
COMPASS_TRAINING_DATA   = "Compass.txt"
GROUND_TRUTH_DATA_RAW   = "Ground Truth Raw.txt"
GROUND_TRUTH_DATA       = "Ground Truth.txt"

NUM_TEST_FILES          = 5
TRAINED_NN_FILE         = "trained network/trained_network.xml"
MAX_FEATURE_FILE        = "trained network/max_features.txt"
MIN_FEATURE_FILE        = "trained network/min_features.txt"

# step detection with real data
STEP_DETECTION_DATA_LOCATION    = "real data"
ACCEL_STEP_DETECTION_DATA       = "Accel.txt"
GYRO_STEP_DETECTION_DATA        = "Gyro.txt"
COMPASS_STEP_DETECTION_DATA     = "Compass.txt"