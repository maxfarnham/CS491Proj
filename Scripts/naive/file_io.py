import csv, text_manip, os, fnmatch
def loadCsv(filename):
	lines = csv.reader(open(filename, "rb"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def recGetFilesByExtension(directory,extension):
	matches = []
	for root, dirnames, filenames in os.walk(directory):
	  for filename in fnmatch.filter(filenames, '*.' + extension):
	    matches.append(os.path.join(root, filename))
	return matches

def concat_html_file_text(source, destination):
	files = recGetFilesByExtension(source, 'htm')
	textfile = open(destination, 'a+')              
	for filename in files: 
		with open (filename, "r") as htmlfile:
			textfile.write(text_manip.html_to_words(htmlfile.read()) + '\n')  

def create_training_file(destination):
	source = 'C:/Users/William/CS491Proj/Corpus/NotNews'
	label = 0
	files = recGetFilesByExtension(source, 'htm')
	textfile = open(destination, 'a+')              
	for filename in files: 
		with open (filename, "r") as htmlfile:
			textfile.write(text_manip.create_simple_feature_vector(htmlfile.read()) + str(label) + '\n')  
	source = 'C:/Users/William/CS491Proj/Corpus/News'
	label = 1
	files = recGetFilesByExtension(source, 'htm')
	textfile = open(destination, 'a+')              
	for filename in files: 
		with open (filename, "r") as htmlfile:
			textfile.write(text_manip.create_simple_feature_vector(htmlfile.read()) + str(label) + '\n')  