# -*- coding: utf-8 -*-
"""Assignment 1 - Wine Quality.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TOsBnG8WIAztPHwrrcRTJAQ02fMcuJQL
"""

#Made By: Hamdy Osama Mohammed Elsayed Farag
#ID     : 2100966
#Course : CSE 616 

import numpy as np
import csv
import matplotlib.pyplot as plt

#loading wine data from the csv file
file = open("winequality-red.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
file.close()
data=np.genfromtxt('winequality-red.csv',delimiter=';',skip_header=1)
#verifying loading data successfully
print(data)

#shuffling data before separating training and testing datasets
data_shuffled = data
# Having a fixed seed enables reproducing the same random results everytime the code is run
np.random.seed(1)
np.random.shuffle(data_shuffled)
#50% of data will be used for training
training_data, testing_data = data_shuffled[:int(len(data_shuffled)/2),:], data_shuffled[int(len(data_shuffled)/2):,:]

# Dividing the given data into inputs and corresponding ground truth classifications
input_training_data = training_data[:,0:11]
truth_training_data = np.reshape(training_data[:,11],[len(training_data),1])



#changing the output format into different classes with binary values

#making a matrix full of zeros
truth_training_classification = np.zeros([len(input_training_data),11])

#placing 1 in the index of the right classification
for training_example in range(0,len(input_training_data)):
  truth_training_classification[training_example][int(truth_training_data[training_example][0])]=1

#Data Preprocessing (Standardizing data)

#calculating mean and std for each feature vector
training_mean = np.mean(input_training_data, axis = 0)
training_std = np.std(input_training_data, axis = 0)
#standardizing data (x-mean)/std
standardized_training_set=(input_training_data-training_mean)/training_std
#appending "1" for each feature vector as a bias
final_training_set=np.append(standardized_training_set,[[1,1,1,1,1,1,1,1,1,1,1]], axis = 0)

def sigmoid(z):
   

    #from the definition of the sigmoid function
    s = 1/(1+np.exp(-z))
    
    
    return s

def ReLU(x):
    return x * (x > 0)

def relu_backward(dout, cache):
    x = cache
    dx = np.where(x > 0, dout, 0)
    return dx

def sigmoid_backward(dA, cache):
    
    Z = cache 
    s = sigmoid(Z)
    #from the definition of the derivative of sigmoid, and using the chain rule to get dZ
    dZ = dA * s * (1-s)
    return dZ

def initialize_parameters_deep(layer_dims):
   
   # The layer_dims argument is an array having the number of nodes in each layer
    np.random.seed(1)
    parameters = {}
    L = len(layer_dims)            # number of layers in the network

    for l in range(1, L):
        #dimension of weights between 2 fully connected layers = (layer_dims[l],layer_dims[l-1])
        parameters['W' + str(l)] = np.random.randn(layer_dims[l],layer_dims[l-1]) * 0.01
        #bias is found only once in the input of each node in a layer
        parameters['b' + str(l)] = np.zeros((layer_dims[l],1))
        

    return parameters

def linear_activation_forward(A_prev, W, b, activation):
    
    # Implement the forward propagation for the LINEAR->ACTIVATION sigmoid layer

    # Arguments:
    # A_prev -- activations from previous layer (or input data): (size of previous layer, number of examples)
    # W -- weights matrix: numpy array of shape (size of current layer, size of previous layer)
    # b -- bias vector, numpy array of shape (size of the current layer, 1)
    

    # Returns:
    # A -- the output of the activation function
    # cache -- a python tuple containing values used for later use in back propagation
             
    
    
    # Inputs: "A_prev, W, b". Outputs: "A, cache".
    #linear function of multiplying inputs by weights and adding bias
    Z = np.dot(W,A_prev) + b 

    if activation =="sigmoid":
    #performing activation function of sigmoid
      A = sigmoid(Z) 

    elif activation == "relu":
      A = ReLU(Z)

    cache = ((A_prev, W, b), Z)

    return A, cache

def L_model_forward(X, parameters):
    
    # Implement forward propagation for the whole network (single forward pass)
    
    # Arguments:
    # X -- data, numpy array of shape (input size, number of examples) training data
    # parameters -- output of initialize_parameters_deep()
    
    # Returns:
    # AL -- last post-activation value
    # caches -- list of caches containing:
    #           every cache of linear_activation_forward() (there are L-1 of them, indexed from 0 to L-1)
    

    caches = []
    A = X
    L = len(parameters) // 2                  # number of layers in the neural network
 
    for l in range(1, L):
        A_prev = A 
        A, cache = linear_activation_forward(A_prev, parameters['W' + str(l)], parameters['b' + str(l)],"relu")
        caches.append(cache)
    #output layer
    A_prev = A 
    A, cache = linear_activation_forward(A_prev, parameters['W' + str(L)], parameters['b' + str(L)],"sigmoid")
    caches.append(cache)   
    
            
    return A, caches

def compute_cost(AL, Y):
   
    #Implement the cost function defined by cross entropy equation.

    # Arguments:
    # AL -- probability vector corresponding to your label predictions, shape (1, number of examples)
    # Y -- true "label" vector 

    # Returns:
    # cost -- categorial cross-entropy cost
    
    # code commented by ## is used for the cross entropy cost (binary)
   ## m = Y.shape[1]

    # Compute loss from aL and y.
    
    ##cost = (-1/m) * (np.dot(Y, np.log(AL.T)))
    
    loss = 0.0
    for true, pred in zip(Y, AL):
      loss += np.log(pred[int(true)-1])
    cost = 1 * loss / len(Y)

    
    
    
    return cost

def linear_backward(dZ, cache):
    # Here cache is "linear_cache" containing (A_prev, W, b) coming from the forward propagation in the current layer
    """
    Implement the linear portion of backward propagation for a single layer (layer l)

    Arguments:
    dZ -- Gradient of the cost with respect to the linear output (of current layer l)
    cache -- tuple of values (A_prev, W, b) coming from the forward propagation in the current layer

    Returns:
    dA_prev -- Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
    dW -- Gradient of the cost with respect to W (current layer l), same shape as W
    db -- Gradient of the cost with respect to b (current layer l), same shape as b
    """
    A_prev, W, b = cache
    m = A_prev.shape[1]

   
    dW = (1/m) * np.dot(dZ, A_prev.T)
    db = (1/m) * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T,dZ)
   
    
    assert (dA_prev.shape == A_prev.shape)
    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)
    
    return dA_prev, dW, db

def linear_activation_backward(dA, cache, activation):
    """
    Implement the backward propagation for the LINEAR->ACTIVATION layer.
    
    Arguments:
    dA -- post-activation gradient for current layer l 
    cache -- tuple of values (linear_cache, activation_cache) we store for computing backward propagation efficiently
    activation -- the activation to be used in this layer, stored as a text string: "sigmoid" or "relu"
    
    Returns:
    dA_prev -- Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
    dW -- Gradient of the cost with respect to W (current layer l), same shape as W
    db -- Gradient of the cost with respect to b (current layer l), same shape as b
    """
    linear_cache, activation_cache = cache
    
    if activation == "relu":
        ### START CODE HERE ### (??? 1 line of code)
        dZ = relu_backward(dA, activation_cache)
        ### END CODE HERE ###
        
    elif activation == "sigmoid":
        ### START CODE HERE ### (??? 1 line of code)
        dZ = sigmoid_backward(dA, activation_cache)
        ### END CODE HERE ###
    
    ### START CODE HERE ### (??? 1 line of code)
    dA_prev, dW, db = linear_backward(dZ, linear_cache)
    ### END CODE HERE ###
    
    return dA_prev, dW, db

def L_model_backward(AL, Y, caches):
    """
    Implement the backward propagation for the [LINEAR->RELU] * (L-1) -> LINEAR -> SIGMOID group
    
    Arguments:
    AL -- probability vector, output of the forward propagation (L_model_forward())
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat)
    caches -- list of caches containing:
                every cache of linear_activation_forward() with "relu" (it's caches[l], for l in range(L-1) i.e l = 0...L-2)
                the cache of linear_activation_forward() with "sigmoid" (it's caches[L-1])
    
    Returns:
    grads -- A dictionary with the gradients
             grads["dA" + str(l)] = ... 
             grads["dW" + str(l)] = ...
             grads["db" + str(l)] = ... 
    """
    grads = {}
    L = len(caches) # the number of layers
    m = AL.shape[1]
    Y = Y.reshape(AL.shape) # after this line, Y is the same shape as AL
    
    # Initializing the backpropagation
    ### START CODE HERE ### (1 line of code)
    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    ### END CODE HERE ###
    
    # Lth layer (SIGMOID -> LINEAR) gradients. Inputs: "dAL, current_cache". Outputs: "grads["dAL-1"], grads["dWL"], grads["dbL"]
    ### START CODE HERE ### (approx. 2 lines)
    current_cache = caches[L-1] # Last Layer
    grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache,"sigmoid")
    ### END CODE HERE ###
    
    # Loop from l=L-2 to l=0
    for l in reversed(range(L-1)):
        # lth layer: (Sigmoid -> LINEAR) gradients.
        # Inputs: "grads["dA" + str(l + 1)], current_cache". Outputs: "grads["dA" + str(l)] , grads["dW" + str(l + 1)] , grads["db" + str(l + 1)] 
        ### START CODE HERE ### (approx. 5 lines)
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 1)], current_cache,"relu")
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp
        ### END CODE HERE ###

    return grads

def update_parameters(parameters, grads, learning_rate):
    """
    Update parameters using gradient descent
    
    Arguments:
    parameters -- python dictionary containing your parameters 
    grads -- python dictionary containing your gradients, output of L_model_backward
    
    Returns:
    parameters -- python dictionary containing your updated parameters 
                  parameters["W" + str(l)] = ... 
                  parameters["b" + str(l)] = ...
    """
    
    L = len(parameters) // 2 # number of layers in the neural network

    # Update rule for each parameter. Use a for loop.
    ### START CODE HERE ### (??? 3 lines of code)
    for l in range(L):
        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - learning_rate * grads["dW" + str(l+1)]
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - learning_rate * grads["db" + str(l+1)]
    ### END CODE HERE ###
    return parameters

def L_layer_model(X, Y_hot, Y, layers_dims, learning_rate = 0.0075, num_iterations = 3000, print_cost=False):#lr was 0.009
    """
    Implements a L-layer neural network: [LINEAR->sigmoid]*(L-1)->LINEAR->SIGMOID.
    
    Arguments:
    X -- data, numpy array for training
    Y -- true "label" vector 
    layers_dims -- list containing the input size and each layer size, of length (number of layers + 1).
    learning_rate -- learning rate of the gradient descent update rule
    num_iterations -- number of iterations of the optimization loop
    print_cost -- if True, it prints the cost every 100 steps
    
    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """

    np.random.seed(1)
    costs = []                         # keep track of cost
    
    # Parameters initialization. (??? 1 line of code)
    ### START CODE HERE ###
    parameters = initialize_parameters_deep(layers_dims)
    ### END CODE HERE ###
    
    # Loop (gradient descent)
    for i in range(0, num_iterations):

        # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
        ### START CODE HERE ### (??? 1 line of code)
        AL, caches = L_model_forward(X, parameters)
        ### END CODE HERE ###
        
        # Compute cost.
        ### START CODE HERE ### (??? 1 line of code)
        cost = compute_cost(AL, Y)
        ### END CODE HERE ###
    
        # Backward propagation.
        ### START CODE HERE ### (??? 1 line of code)
        grads = L_model_backward(AL, Y_hot, caches)
        ### END CODE HERE ###
 
        # Update parameters.
        ### START CODE HERE ### (??? 1 line of code)
        parameters = update_parameters(parameters, grads, learning_rate)
        ### END CODE HERE ###
                
        # Print the cost every 100 training example
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)
            
    # plot the cost
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per hundreds)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()

    plt.plot(np.sum((AL-Y_hot),axis = 0))
    plt.xlim([0, 789])
    #plt.ylim([-0.5, 1])
    plt.ylabel('error')
    plt.xlabel('iterations ')
    plt.title('error')
    plt.show()
    print(AL)
    

    return parameters

#training the model and getting parameters to be used in testing

#getting the real wine quality from training data

ground_truth = np.reshape(np.append(training_data[:,11],[1]),[800,1])

ground_truth_hot = np.reshape(np.append(truth_training_classification,[1,1,1,1,1,1,1,1,1,1,1]),[800,11])

parameters=L_layer_model(final_training_set.T, ground_truth_hot.T, ground_truth, [11,30,11], learning_rate = 0.00001, num_iterations = 1000, print_cost=True)

#testing the model using the testing_data set and the trained parameters

prediction,cache = L_model_forward(testing_data[:,0:11].T,parameters)

#making a matrix full of zeros
truth_testing_classification = np.zeros([len(testing_data),11])

#placing 1 in the index of the right classification
for testing_example in range(0,len(testing_data)):
  truth_testing_classification[testing_example][int(testing_data[:,11:12][testing_example][0])]=1

RMSE=np.sqrt(np.square(np.subtract(truth_testing_classification,prediction.T)).mean() )

print(prediction.T[1])
print(truth_testing_classification[1])
RMSE