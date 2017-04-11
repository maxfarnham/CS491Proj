from os import path
import time

positive_label = 'news'
featuresOn = True
svmpickle = 'svmpickle.pkl'

spider_dir = path.abspath(r'C:\dev\projects\Spider\CS491Proj\491_Spider')
news_dir = path.abspath(r'C:\dev\projects\Spider\CS491Proj\Corpus\News')
not_news_dir = path.abspath(r'C:\dev\projects\Spider\CS491Proj\Corpus\notNews')

classified_positive = path.abspath(r'C:\dev\projects\Spider\CS491Proj\classifications\pos')
classified_negative = path.abspath(r'C:\dev\projects\Spider\CS491Proj\classifications\neg')

newsspace = path.abspath('Corpus/newsspace200.xml/newsspace200.xml')

intersector_path = path.abspath('frankenfile.txt')
featureFile = 'features.csv'
lda_log = time.strftime("%Y%m%d-%H%M%S").join(('lda_log','.txt'))


