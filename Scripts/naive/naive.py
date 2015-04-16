import dataset_utilities as du
import file_io as fi
import text_manip as tm
def naive_bayes(featureFile):
	fi.create_training_file(featureFile)
	splitRatio = 0.67
	dataset = fi.loadCsv(featureFile)
	trainingSet, testSet = du.splitDataset(dataset, splitRatio)
	print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
	# prepare model
	summaries = du.summarizeByClass(trainingSet)
	# test model
	predictions = du.getPredictions(summaries, testSet)
	accuracy = du.getAccuracy(testSet, predictions)
	print('Accuracy: {0}%').format(accuracy)