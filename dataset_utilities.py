import random, math
#http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated

def mean(numbers):
	return sum(numbers)/float(len(numbers))
 
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)

def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries

def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	summaries = {}
	for classValue, instances in separated.iteritems():
		summaries[classValue] = summarize(instances)
	return summaries

def calculateGaussianProbability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.iteritems():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateGaussianProbability(x, mean, stdev)
	return probabilities

def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.iteritems():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def bag_of_words(training_set):
    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.  
    vectorizer = CountVectorizer(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = None) 
    
    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of 
    # strings.
    train_data_features = vectorizer.fit_transform(training_set)
    
    # Numpy arrays are easy to work with, so convert the result to an 
    # array
    train_data_features = train_data_features.toarray()

def create_simple_feature_vector(raw_html):
    countPeriod = 0
    countComma = 0
    countQuestion = 0
    countExclamation = 0
    countWspace = 0
    countLetters = 0
    longestWordLength = 0
    currentWordLength = 0
    for letter in raw_html:
        countLetters+=1
        if letter == '.':
            countPeriod+=1
        if letter == ',':
            countComma+=1
        if letter == '?':
            countQuestion+=1
        if letter == '!':
            countExclamation+=1
        if letter == ' ':
            countWspace+=1
            if currentWordLength > longestWordLength:
                longestWordLength = currentWordLength
            currentWordLength = 0            
        else:
            currentWordLength+=1
    #return str(countPeriod) + ',' + str(countComma) + ',' + str(countQuestion) + ',' + str(countExclamation) + ',' + str(countLetters) + ',' + str(longestWordLength) + ',' + str(countWspace) + ','
    return str(binarize(countPeriod, 4893)) + ',' + str(binarize(countComma, 1130)) + ',' + str(binarize(countQuestion, 153)) + ',' + str(binarize(countExclamation, 202)) + ',' + str(binarize(countLetters, 362823)) + ',' + str(binarize(longestWordLength, 907)) + ',' + str(binarize(countWspace, 26985)) + ','
    
def binarize(observation, threshold):
	return 1 if observation > threshold else 0	



