from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from scipy import diag
from numpy.random import multivariate_normal

means = [(-1,0),(2,4),(3,1)]
cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
alldata = ClassificationDataSet(2, 1, nb_classes=3)
for n in xrange(400):
  for klass in range(3):
    input = multivariate_normal(means[klass],cov[klass])
    alldata.addSample(input, [klass])

# getting train dataset and test dataset
tstdata_temp, trndata_temp = alldata.splitWithProportion(0.25)

tstdata = ClassificationDataSet(2, 1, nb_classes=3)
for n in xrange(0, tstdata_temp.getLength()):
  tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )

trndata = ClassificationDataSet(2, 1, nb_classes=3)
for n in xrange(0, trndata_temp.getLength()):
  trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )


print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]

fnn = buildNetwork( trndata.indim, 5, trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

for i in range(1000):
  trainer.trainEpochs( 1 )
  trnresult = percentError( trainer.testOnClassData(), trndata['class'] )
  tstresult = percentError( trainer.testOnClassData(dataset=tstdata), tstdata['class'] )

  print "epoch: %4d" % trainer.totalepochs, \
        "  train error: %5.2f%%" % trnresult, \
        "  test error: %5.2f%%" % tstresult