from os import path
import time

featuresOn = True
svmpickle = 'svmpickle.pkl'

news_dir = path.abspath(r'C:\Users\William\Desktop\CS491Proj\Corpus\News')
not_news_dir = path.abspath(r'C:\Users\William\Desktop\CS491Proj\Corpus\notNews')

newsspace = path.abspath('Corpus/newsspace200.xml/newsspace200.xml')

intersector_path = path.abspath('frankenfile.txt')
featureFile = 'features.csv'
lda_log = time.strftime("%Y%m%d-%H%M%S").join(('lda_log','.txt'))


