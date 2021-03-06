'''
Class for defining a normal random variable
'''

import numpy as np
from scipy.stats import norm as scipynormal


class NormalRandomVariable(object):
    '''
    Class for defining a normal random variable
    '''

    def __init__(self, mean=0., std_dev=1.0, max_moment=10):
        '''
        Initialize the normal (gaussian) random variable with provided mean
        and standard deviation. Implementation wraps scipy.stats.norm to get
        statistics/samples.
        '''

        if std_dev <= 0:
            raise ValueError("Normal standard deviation  must be positive")

        self._mean = mean
        self._std = std_dev

        #set dimension (scalar), min/max to equal mean +/- 4stds
        self._dim = 1
        self._mins = [mean - 4.*std_dev]
        self._maxs = [mean + 4.*std_dev]

        #cache moments
        self.generate_moments(max_moment)
        self._max_moment = max_moment

    def get_variance(self):
        '''
        Returns variance of normal random variable
        '''
        return self._std**2.0

    def compute_moments(self, max_order):
        '''
        Returns moments up to order 'max_order' in numpy array.
        '''

        #TODO - calculate moments above max_moment on the fly & append to stored
        if max_order <= self._max_moment:
            moments = self._moments[:max_order]
        else:
            raise NotImplementedError("Moment above max_moment not handled yet")

        return moments


    def compute_CDF(self, x_grid):
        '''
        Returns numpy array of normal CDF values at the points contained
        in x_grid
        '''

        return scipynormal.cdf(x_grid, self._mean, self._std)


    def compute_inv_CDF(self, x_grid):
        '''
        Returns np array of inverse normal CDF values at pts in x_grid
        '''
        return scipynormal.ppf(x_grid, self._mean, self._std)


    def compute_pdf(self, x_grid):
        '''
        Returns numpy array of normal pdf values at the points contained
        in x_grid
        '''
        return scipynormal.pdf(x_grid, self._mean, self._std)


    def draw_random_sample(self, sample_size):
        '''
        Draws random samples from the normal random variable. Returns numpy
        array of length 'sample_size' containing these samples
        '''

        #Use scipy normal rv to return shifted/scaled samples automatically
        return scipynormal.rvs(self._mean, self._std, sample_size)

    def generate_moments(self, max_moment):
        '''
        Calculate & store moments to retrieve more efficiently later
        '''

        self._moments = np.zeros((max_moment, 1))

        #Rely on scipy.stats to return non-central moment
        for i in range(max_moment):
            self._moments[i] = scipynormal.moment(i+1, self._mean, self._std)


