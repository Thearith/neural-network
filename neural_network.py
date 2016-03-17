from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from feature_extraction          import extract_features_from_data
import file_reader_writer        as file

# CONSTANTS
ACCEL_TRAINING_DATA   = "training/March 14 2016 - 19-17-55-698 - Accel.txt"
GYRO_TRAINING_DATA    = "training/March 14 2016 _ 19_17_55_698 - Gyro.txt"
COMPASS_TRAINING_DATA = "training/March 14 2016 _ 19_17_55_698 - Compass.txt"

NUM_CLASSES         = 2
HIDDEN_UNITS        = 5
TRAINING_ITERATION  = 20
NUM_EPOCHS          = 1


if __name__ == "__main__":

  # read file
  accel_list = file.get_sensor_list(ACCEL_TRAINING_DATA)
  gyro_list = file.get_sensor_list(GYRO_TRAINING_DATA)
  compass_list = file.get_sensor_list(COMPASS_TRAINING_DATA)


  # feature extraction
  print "\n"
  print "********************* FEATURE EXTRACTION *********************"
  features = extract_features_from_data(accel_list, gyro_list, compass_list)
  input = [ features[i][0] for i in range(len(features))]
  output = [ features[i][1] for i in range(len(features))]
  num_features = len(input[0])
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
  fnn = buildNetwork( trndata.indim, HIDDEN_UNITS, trndata.outdim, outclass=SoftmaxLayer )
  trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

  print "********************* TRAINING DATA *********************"

  for i in range(TRAINING_ITERATION):
    trainer.trainEpochs(NUM_EPOCHS)
    trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(dataset=tstdata), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult

  print "\n\n"
  print "********************* TRAINED NEURAL NETWORK *********************"
  print fnn, "\n"