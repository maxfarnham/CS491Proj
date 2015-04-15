import file_io, dataset_utilities
def main():
	#handle data
	filename = 'pima-indians-diabetes.data.csv'
	dataset = file_io.loadCsv(filename)
	print('Loaded data file {0} with {1} rows').format(filename, len(dataset))

	dataset = [[1], [2], [3], [4], [5]]
	splitRatio = 0.67
	train, test = dataset_utilities.splitDataset(dataset, splitRatio)
	print('Split {0} rows into train with {1} and test with {2}').format(len(dataset), train, test)

	#summarize data
	dataset = [[1,20,1], [2,21,0], [3,22,1]]
	separated = dataset_utilities.separateByClass(dataset)
	print('Separated instances: {0}').format(separated)

	numbers = [1,2,3,4,5]
	print('Summary of {0}: mean={1}, stdev={2}').format(numbers, dataset_utilities.mean(numbers), dataset_utilities.stdev(numbers))
	
	dataset = [[1,20,0], [2,21,1], [3,22,0]]
	summary = dataset_utilities.summarize(dataset)
	print('Attribute summaries: {0}').format(summary)

	dataset = [[1,20,1], [2,21,0], [3,22,1], [4,22,0]]
	summary = dataset_utilities.summarizeByClass(dataset)
	print('Summary by class value: {0}').format(summary)

	#make a prediction
	x = 71.5
	mean = 73
	stdev = 6.2
	probability = dataset_utilities.calculateProbability(x, mean, stdev)
	print('Probability of belonging to this class: {0}').format(probability)

	summaries = {0:[(1, 0.5)], 1:[(20, 5.0)]}
	inputVector = [1.1, '?']
	probabilities = dataset_utilities.calculateClassProbabilities(summaries, inputVector)
	print('Probabilities for each class: {0}').format(probabilities)

	summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
	inputVector = [1.1, '?']
	result = predict(summaries, inputVector)
	print('Prediction: {0}').format(result)

	#make predictions 
	summaries = {'A':[(1, 0.5)], 'B':[(20, 5.0)]}
	testSet = [[1.1, '?'], [19.1, '?']]
	predictions = getPredictions(summaries, testSet)
	print('Predictions: {0}').format(predictions)

	#get accuracy
	testSet = [[1,1,1,'a'], [2,2,2,'a'], [3,3,3,'b']]
	predictions = ['a', 'a', 'a']
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: {0}').format(accuracy)

	
