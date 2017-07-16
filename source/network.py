"""
netural network
optimzied with stochatic gradient
"""

# Third party libary 
import numpy as np 
import random 

class QuadraticCost(object):
    
    @staticmethod
    def cost(a, y):
        return 0.5 * (np.linalg.norm(a - y)**2)

    @staticmethod
    def delta(z, a, y):
        return (a - y) * sigmoid_prime(z)


class CrossEntropyCost(object):

    @staticmethod
    def cost(a, y):
        return np.nan_to_num(-y * np.log(a) - (1-y)*np.log(1-a))

    @staticmethod
    def delta(z, a, y):
        return (a - y) 


def sigmoid(z):
    return (1.0/(1.0 + np.exp(-z)))


def sigmoid_prime(z):
    """Derivation of the sigmoid function"""
    return sigmoid(z)*(1 - sigmoid(z))


class Network(object):
    """ Represents a netural network with :
    1. sizes[i]: the number of neurons in the ith layer
    2. biases[i]: the biases of the ith layer
    3. wts[i][j][k]: the wt from the kth neuron in the ith
    layer to the jth neuron in the (i+1)th layer
    Initially all are random values.
    A netural network is initialized as Network(sizes)
    """

    def __init__(self, sizes = None, cost = CrossEntropy, customValues = None):
        if not customValues:
            self.layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(x, 1) for x in sizes[1:]]
            self.wts = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        else:
            self.sizes, self.biases, self.wts = customValues
        self.cost = cost


    def feedforward(self, inputs):
        """ Retrun
                
