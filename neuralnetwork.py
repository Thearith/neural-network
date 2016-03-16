from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

# CONSTANTS
FILE_NAME           = "training/training.txt"

NUM_FEATURES        = 3
NUM_CLASSES         = 2
HIDDEN_UNITS        = 5
TRAINING_ITERATION  = 20
NUM_EPOCHS          = 1

# read file
input = []
output = []
with open(FILE_NAME, 'r') as reader:
  for line_terminated in reader:
    line = line_terminated.rstrip('\n')
    words = line.split()
    input.append(words[0:NUM_FEATURES])
    output.append(words[-1])


# dataset
alldata = ClassificationDataSet(NUM_FEATURES, 1, nb_classes=NUM_CLASSES)
for n in range(len(input)):
  alldata.addSample(input[n], [output[n]])

# getting train dataset and test dataset
tstdata_temp, trndata_temp = alldata.splitWithProportion(0.25)

tstdata = ClassificationDataSet(NUM_FEATURES, 1, nb_classes=NUM_CLASSES)
for n in xrange(0, tstdata_temp.getLength()):
  tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )

trndata = ClassificationDataSet(NUM_FEATURES, 1, nb_classes=NUM_CLASSES)
for n in xrange(0, trndata_temp.getLength()):
  trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )


print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]

# build network
fnn = buildNetwork( trndata.indim, HIDDEN_UNITS, trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

for i in range(TRAINING_ITERATION):
  trainer.trainEpochs( NUM_EPOCHS )
  trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
  tstresult = percentError( trainer.testOnClassData(dataset=tstdata), tstdata['class'] )

  print "epoch: %4d" % trainer.totalepochs, \
        "  train error: %5.2f%%" % trnresult, \
        "  test error: %5.2f%%" % tstresult

print fnn