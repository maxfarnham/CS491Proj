import csv, text_manip, os, fnmatch
import local as loc
import dataset_utilities as du
import re
from bs4 import BeautifulSoup as bs
import os, errno

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured
def getCategoriesFromXML(file=loc.newsspace):
    categoryDict = dict()
    with open(file, 'r') as xf:
        xml = xf.read()
        #soup = bs(xml)
        #takeaways = soup.findAll('category')
        cats = re.findall(r'<category>(.*?)<',xml)
        for cat in cats:
            if cat not in categoryDict:
                categoryDict[cat] = 1
            else:
                categoryDict[cat] += 1
        for key in categoryDict.keys():
            if categoryDict[key] < 107:
                categoryDict.pop(key, None)
        return categoryDict
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
	textfile = open(destination, 'w+')
	textfile.write('periodRatio,countComma,countLetters,longestWordLength,countWspace,class\n')
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

if __name__ == "__main__":
    tags = getCategoriesFromXML()