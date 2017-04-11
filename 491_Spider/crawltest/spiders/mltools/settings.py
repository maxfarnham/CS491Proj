from os import path
import time

positive_label = 'news'
featuresOn = True
svmpickle = 'svmpickle.pkl'

spider_dir = path.abspath(r'/spider/491_Spider')
news_dir = path.abspath(r'/spider/Corpus/News')
not_news_dir = path.abspath(r'/spider/Corpus/NotNews')

classified_positive = path.abspath(r'/spider/classifications/pos')
classified_negative = path.abspath(r'/spider/classifications/neg')

newsspace = path.abspath('/spider/Corpus/newsspace200.xml/newsspace200.xml')

intersector_path = path.abspath('/spider/frankenfile.txt')
featureFile = '/spider/features.csv'
lda_log = time.strftime("%Y%m%d-%H%M%S").join(('lda_log','.txt'))


