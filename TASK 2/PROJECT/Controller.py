from numpy.random import random_integers
import pandas as pd
import random
import tkinter as tk
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sklearn as sk
from enum import Enum
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import time
import math
from matplotlib import colors
import DataModel

def sum_of_array(an_array):
    sum = 0 
    for i in an_array:
        sum += i
    return sum

if __name__ == '__main__':
    new_model = DataModel.DataModel()

    new_array = []
    pred_vals = new_model.linear_regression_model.predict(new_model.test_set)

    for i in range(0,len(pred_vals)):
        new_array.append(abs(new_model.kmeans_test_set[i] - pred_vals[i]))

    print(max(new_model.kmeans_test_set))
    print(min(new_model.kmeans_test_set))
    print(max(pred_vals))
    print(min(pred_vals))
    print(sum_of_array(new_array)/len(new_array))

    plt.scatter(pred_vals, new_model.kmeans_test_set, c=new_model.kmeans_test_set, s=5, alpha=.2, marker='o', cmap=new_model.cmap)
    plt.plot(pred_vals, pred_vals, '-')
    plt.show()

    plt.scatter(new_model.train_set.iloc[:, 0], new_model.train_set.iloc[:, 1], c=new_model.kmeans_data_set, s=1, alpha=.4, cmap=new_model.cmap)

    centers = new_model.kmeans_model.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=0.5);
    plt.plot(range(-20,20), [0]*40, '-', linewidth=1)
    plt.plot( [0]*40, range(-20,20), '-', linewidth=1)
    plt.show()


