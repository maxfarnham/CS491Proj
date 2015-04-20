import csv, text_manip, os, fnmatch
import local as loc
import dataset_utilities as du
def loadCsv(filename, ignoreHeaders=True):
	lines = csv.reader(open(filename, "rb"))
	if ignoreHeaders:
		next(lines, None)
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def recGetFiles(directory,extension='htm'):
	matches = []
	for root, dirnames, filenames in os.walk(directory):
	  for filename in fnmatch.filter(filenames, '*.' + extension):
		matches.append(os.path.join(root, filename))
	return matches

def getTopLevelFiles(directory, extension='htm'):
	matches = []
	for file in os.listdir(directory):
		if file.endswith("." + extension):
			matches.append(os.path.join(directory, file))
	return matches

def concat_html_file_text(source, destination):
	files = recGetFiles(source, 'htm')
	textfile = open(destination, 'a+')              
	for filename in files: 
		with open (filename, "r") as htmlfile:
			textfile.write(text_manip.html_to_words(htmlfile.read()) + '\n')  

def create_training_file(destination = loc.featureFile):
	source = loc.not_news_dir
	label = 0
	files = getTopLevelFiles(source, 'htm')
	textfile = open(destination, 'a+')
	textfile.write('countPeriod, countComma, countQuestion, countExclamation, countLetters, longestWordLength, countWspace, class\n')
	for filename in files: 
		with open (filename, "r") as htmlfile:
			print(filename)
			textfile.write(du.create_simple_feature_vector(htmlfile.read()) + str(label) + '\n')  
	source = loc.news_dir
	label = 1
	files = getTopLevelFiles(source, 'htm')
	textfile = open(destination, 'a+')              
	for filename in files: 
		with open (filename, "r") as htmlfile:
			print(filename)
			textfile.write(du.create_simple_feature_vector(htmlfile.read()) + str(label) + '\n')  