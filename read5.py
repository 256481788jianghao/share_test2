import pandas as pd
import tushare as ts
import os
import matplotlib.pyplot as plt
import datetime
import math
import tensorflow as tf
import numpy as np
import random
import sqlite3

ts.set_token('edd599506620c2fa4466f6ff765ff458d3dd894b136356c68b8baa32')
ts_api = ts.pro_api()

data = ts.pro_bar(pro_api=ts_api, ts_code='601878.SH', adj='qfq',freq='D')
print(data)
