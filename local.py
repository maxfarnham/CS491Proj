from os import path
import time


news_dir = path.abspath('corpus/news')
not_news_dir = path.abspath('corpus/news')

newsspace = path.abspath('Corpus/newsspace200.xml/newsspace200.xml')

intersector_path = path.abspath('frankenfile.txt')
featureFile = 'features.csv'
lda_log = time.strftime("%Y%m%d-%H%M%S").join(('lda_log','.txt'))


