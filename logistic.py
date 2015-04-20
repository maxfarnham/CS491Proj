import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import local as loc
import statsmodels.discrete.discrete_model as ddm

#read the data if __name__ == '__main__':
#data file should be a csv in the format:
#class,feature1,feature2,...,featureN
#with first row a header row
def demo(featureFile=loc.featureFile):
    dataset = pd.read_csv(featureFile)
    #print df.describe()
    #print df.std()
    ##df.hist()
    #pl.show()
    dataset['intercept'] = 1.0
    train_cols = dataset.columns[0:len(dataset.columns)-1]
    #logit = sm.Logit(dataset['class'], dataset[train_cols])
    logit = ddm.Logit(dataset['class'], dataset[train_cols])
    #result = logit.fit()
    result = logit.fit_regularized()
    print result.summary()
    
	