# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
    AccCount = -1 # Aaccuracy for each set
    rawPrior = util.Counter() # probability for each label
    rawCondProb = util.Counter() # Conditional probability of feature 
    rawCounts = util.Counter() # counts for each feature  in each label
    for i in range(len(trainingData)):
        datum = trainingData[i]
        label = trainingLabels[i]
        rawPrior[label] += 1
        for feat, value in datum.items():
            rawCounts[(feat,label)] += 1
            if value > 0: 
                rawCondProb[(feat, label)] += 1
    # Smoothing parameter 
    for k in kgrid: 
        Prior = util.Counter()
        CondProb = util.Counter()
        Counts = util.Counter()

        for key, val in rawPrior.items():
            Prior[key] += val
        for key, val in rawCounts.items():
            Counts[key] += val
        for key, val in rawCondProb.items():
            CondProb[key] += val

        for label in self.legalLabels:
            for feat in self.features:
                CondProb[ (feat, label)] +=  k
                Counts[(feat, label)] +=  2*k

    # normalize Prior:
        Prior.normalize()
        self.prior = Prior
        for x, count in CondProb.items():
            CondProb[x] = count * 1.0 / Counts[x]
        self.condProb = CondProb

    # check the performance on validation data set
        predictions = self.classify(validationData)
        accuracyCount =  [predictions[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
        rate = 100.0*accuracyCount/len(validationLabels)

        print "For k=%f: (%.1f%%)" % (k, rate)
        if accuracyCount > AccCount:
            bestPrior = Prior
            bestCondProb = CondProb
            bestk = k
            AccCount = accuracyCount
    self.prior = bestPrior
    self.condProb = bestCondProb
    self.k = bestk
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    for label in self.legalLabels:
        logJoint[label] = math.log(self.prior[label])
        for feat, value in datum.items():
            if value > 0:
                logJoint[label] += math.log(self.condProb[feat,label])
            else:
                logJoint[label] += math.log(1-self.condProb[feat,label])    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds
    

    
      
