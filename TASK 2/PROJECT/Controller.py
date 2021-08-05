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

if __name__ == '__main__':
    new_model = DataModel.DataModel()
    print(new_model.get_clean_data())
