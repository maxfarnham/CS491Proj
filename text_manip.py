import re
from bs4 import BeautifulSoup, Comment
#import lxml
#from lxml.html.clean import Cleaner
#import html2text
from nltk.corpus import stopwords
#https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words

@profile
def visible_text(element):
    # dont include non-visible elements
    if element.parent.name in ['style', 'script', 'head']:
        return None
    # don't include comments
    elif isinstance(element, Comment):
        return None
    # if this text is itself HTML, we need to go deeper
    # this is a very naive check and is implemented primarily for speed
    elif re.match('^<\w+?>', element):
        return get_visible_text(element)

    return element

@profile
def get_visible_text(raw_html):
    soup = BeautifulSoup(raw_html).findAll(text=True)
    visible_html = map(visible_text, soup)
    return " ".join([t for t in visible_html if t != None]).encode('UTF-8')

def html_to_words( raw_html ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    #tried this stupid stuff first
    html_text = get_visible_text(raw_html)

    #html_text = html2text.html2text(raw_html.decode('utf-8'))
    
    #
    # 2. Remove non-letters        
    #letters_only = re.sub("[^a-zA-Z]", " ", html_text) 
    #
    # 3. Convert to lower case, split into individual words
    #words = html_text.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    #stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    #meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    #return( " ".join( meaningful_words ))

    return html_text
