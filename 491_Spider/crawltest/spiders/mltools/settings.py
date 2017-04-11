from os import path,getenv
import time

# Docker run command: docker run -v <path to classifications folder on host>:/spider/classifications -e IS_DOCKER='true' <container id> 
if getenv("IS_DOCKER"):
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
else:
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


