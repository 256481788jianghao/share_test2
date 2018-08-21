from readbaseInfo import *
import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math
import tensorflow as tf
import numpy as np
import random


class StockData:
    def __init__(self,codeStr):
        self.codeStr = codeStr
        self.data = readData(codeStr)
        print(self.data)



StockData('300024')
