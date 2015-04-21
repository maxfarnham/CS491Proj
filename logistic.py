import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import local as loc
import scipy 
import statsmodels.discrete.discrete_model as ddm

#read the data if __name__ == '__main__':
#data file should be a csv in the format:
#class,feature1,feature2,...,featureN
#with first row a header row
def demo(featureFile=loc.featureFile):
    dataset = pd.read_csv(featureFile)
    #print dataset.describe()
    #print dataset.std()
    #dataset.hist()
    #pl.show()
    #dataset['intercept'] = 1.0
    train_cols = dataset.columns[0:len(dataset.columns)-1]    
    print('number of cols pre reduce: ' + str(len(dataset[train_cols].columns)))
    arr = independent_columns(dataset[train_cols].as_matrix())
    print('number of cols pre reduce: ' + str(arr.shape[1]))
    #train_cols = dataset.columns[0:len(dataset.columns)-1]

    #logit = sm.Logit(dataset['class'], dataset[train_cols])
    
    #logit = ddm.Logit(dataset['class'], dataset[train_cols])
        
    #result = logit.fit(method='bfgs')
    
    #result = logit.fit_regularized()
    
    #result.predict()
    
    #print result.summary()
    
def independent_columns(A, tol = 1e-05):
    """
    Return an array composed of independent columns of A.

    Note the answer may not be unique; this function returns one of many
    possible answers.

    http://stackoverflow.com/q/13312498/190597 (user1812712)
    http://math.stackexchange.com/a/199132/1140 (Gerry Myerson)
    http://mail.scipy.org/pipermail/numpy-discussion/2008-November/038705.html
        (Anne Archibald)

    >>> A = np.array([(2,4,1,3),(-1,-2,1,0),(0,0,2,2),(3,6,2,5)])
    >>> independent_columns(A)
    np.array([[1, 4],
              [2, 5],
              [3, 6]])
    """
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    return A[:, independent]
    
	