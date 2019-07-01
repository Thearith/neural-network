from pybrain.datasets             import ClassificationDataSet
from pybrain.utilities            import percentError
from pybrain.structure            import SoftmaxLayer, TanhLayer
from pybrain.tools.shortcuts      import buildNetwork
from pybrain.tools.customxml      import NetworkWriter, NetworkReader
from pybrain.supervised.trainers  import BackpropTrainer
from pybrain.structure.modules    import SoftmaxLayer
from feature_extraction           import extract_features_for_training
import file_reader_writer         as file
from constants                    import *

# CONSTANTS
NUM_CLASSES         = 2
HIDDEN_UNITS        = 73
TRAINING_ITERATION  = 1000
ERROR_THRESHOLD     = 0.00001
NUM_EPOCHS          = 1000



if __name__ == "__main__":

  print "\n"
  print "********************* FEATURE EXTRACTION *********************"

  features = []
  for num_file in range(NUM_RAW_FILES):

    # read file
    file_location = TRAINING_DATA_LOCATION + "/" + str(num_file+1) + "/"
    accel_list = file.get_sensor_list(file_location + ACCEL_TRAINING_DATA)
    gyro_list = file.get_sensor_list(file_location + GYRO_TRAINING_DATA)
    compass_list = file.get_sensor_list(file_location + COMPASS_TRAINING_DATA)
    ground_truth_list = file.get_ground_truth(file_location + GROUND_TRUTH_DATA)

    # feature extraction
    feature_list = extract_features_for_training(accel_list, gyro_list, compass_list, ground_truth_list)
    features += feature_list

  input = [ features[i][0] for i in range(len(features))]
  output = [ features[i][1] for i in range(len(features))]
  num_features = len(input[0])
  print "Total Number of Training Data: ", len(features)
  print "Sample Input: " , input[0]
  print "Sample Output: ", output[0], "\n\n"


  # dataset
  alldata = ClassificationDataSet(num_features, 1, nb_classes=NUM_CLASSES)
  for n in range(len(input)):
    alldata.addSample(input[n], output[n])

  # getting train dataset and test dataset
  tstdata_temp, trndata_temp = alldata.splitWithProportion(0.25)

  tstdata = ClassificationDataSet(num_features, 1, nb_classes=NUM_CLASSES)
  for n in xrange(0, tstdata_temp.getLength()):
    tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )

  trndata = ClassificationDataSet(num_features, 1, nb_classes=NUM_CLASSES)
  for n in xrange(0, trndata_temp.getLength()):
    trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

  trndata._convertToOneOfMany( )
  tstdata._convertToOneOfMany( )

  print "********************* TRAINING DATA PATTERN *********************"
  print "Number of training patterns: ", len(trndata)
  print "Input and output dimensions: ", trndata.indim, trndata.outdim
  print "First sample (input, target, class):"
  print trndata['input'][0], trndata['target'][0], trndata['class'][0], "\n\n"


  # build network and train
  fnn = buildNetwork(trndata.indim, HIDDEN_UNITS, trndata.outdim, hiddenclass = TanhLayer, outclass=SoftmaxLayer)
  trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, learningrate=0.001, verbose=True, weightdecay=0.01)

  print "********************* TRAINING DATA *********************"

  for epoch in range(TRAINING_ITERATION):
    error = trainer.train()
    trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(dataset=tstdata), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  error: %.5f" % error, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult


  print "\n\n"
  print "********************* TRAINED NEURAL NETWORK *********************"
  NetworkWriter.writeToFile(fnn, TRAINED_NN_FILE)

  for mod in fnn.modules:
    for conn in fnn.connections[mod]:
      print conn
      for cc in range(len(conn.params)):
        print conn.whichBuffers(cc), conn.params[cc]
  print "\n\n"