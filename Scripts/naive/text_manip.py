import re
#from BeautifulSoup import BeautifulSoup
#import lxml
#from lxml.html.clean import Cleaner
#import html2text
from nltk.corpus import stopwords
#https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words
def html_to_words( raw_html ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    
    #tried this stupid stuff first
    #soup = BeautifulSoup(raw_html)
    #html_text = soup.getText() 
    #cleaner = Cleaner()
    #html_text = cleaner.clean_html(raw_html)

    html_text = ''
    #html2text.html2text(raw_html.decode('utf-8'))
    
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", html_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))

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
    return str(countPeriod) + ',' + str(countComma) + ',' + str(countQuestion) + ',' + str(countExclamation) + ',' + str(countLetters) + ',' + str(longestWordLength) + ',' + str(countWspace) + ','