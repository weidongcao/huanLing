# coding=utf-8
"""
Logistic案例:乳腺癌分类
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
import sklearn
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.linear_model.coordinate_descent import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 设置字符集,防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# 拦截异常
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)

# 数据读取并处理异常数据
path = '/home/dong/opt/document/ai/beifeng_ai/datas/breast-cancer-wisconsin.data'
names = [
    'id',
    'Clump Thickness',
    'Uniformity of Cell Size',
    'Uniformity of Cell Shape',
    'Marginal Adhesion',
    'Single Epithelial Cell Size',
    'Bare Nuclei',
    'Bland Chromatin',
    'Normal Nucleoli',
    'Mitoses',
    'Class'
]

df = pd.read_csv(path, header=None, names=names)

# 只要有列为空,就进行删除操作
datas = df.replace('?', np.nan).dropna(how='any')

# 显示一下
datas.head(5)

datas.dtypes

