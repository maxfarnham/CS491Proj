from os import path
import time


news_dir = path.abspath(r'C:\Users\maxfa_000\Documents\491\Corpus\news')
not_news_dir = path.abspath(r'C:\Users\maxfa_000\Documents\491\Corpus\notnews')

newsspace = path.abspath('Corpus/newsspace200.xml/newsspace200.xml')

intersector_path = path.abspath('frankenfile.txt')
featureFile = 'features.csv'
lda_log = time.strftime("%Y%m%d-%H%M%S").join(('lda_log','.txt'))


