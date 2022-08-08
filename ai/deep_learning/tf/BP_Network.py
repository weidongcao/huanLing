# coding: utf-8
# BP神经网络
# 人数(单位:万人)
import numpy as np
import matplotlib.pyplot as plt

population = [20.55, 22.44, 25.37, 27.13, 29.45, 30.10, 30.96, 34.06, 36.42, 38.09, 39.13, 39.99, 41.93, 44.59, 47.30,
              52.89, 55.73, 56.76, 59.17, 60.63]

# 机动车数(单位:万辆)
vehicle = [0.6, 0.75, 0.85, 0.9, 1.05, 1.35, 1.45, 1.6, 1.7, 1.85, 2.15, 2.2, 2.25, 2.35, 2.5, 2.6, 2.7, 2.85, 2.95,
           3.1]

# 公路面积(单位:万平方公里)
roadarea = [0.09, 0.11, 0.11, 0.14, 0.20, 0.23, 0.23, 0.32, 0.32, 0.34, 0.36, 0.36, 0.38, 0.49, 0.56, 0.59, 0.59, 0.67,
            0.69, 0.79]

# 公路客运量(单位:万人)
passengertraffic = [5126, 6217, 7730, 9145, 10460, 11387, 12353, 15750, 18304, 19836, 21024, 19490, 20433, 22598, 25107,
                    33442, 36836, 40548, 42927, 43462]
# 公路货运量(单位:万吨)
freighttraffic = [1237, 1379, 1385, 1399, 1663, 1714, 1834, 4322, 8132, 8936, 11099, 11203, 10524, 11115, 13320, 16762,
                  18673, 20724, 20803, 21804]

# 合并
samplein = np.mat([population, vehicle, roadarea])
# 2 * 20
sampleout = np.mat([passengertraffic, freighttraffic])


# Max_min标准化
def max_min_normalization(data):
    dataminmax = np.array([data.min(axis=1), data.max(axis=1)])  # 3 * 2 对应最大值最小值
    datanorm = ((np.array(data) - dataminmax[0]) / (dataminmax[1] - dataminmax[0]))
    return datanorm, dataminmax


# 数据标准化
sampleinnorm, sampleinminmax = max_min_normalization(samplein)
sampleoutnorm, sampleoutminmax = max_min_normalization(sampleout)

# 给输出样本添加噪音
noise = 0.03 * np.random.rand(sampleoutnorm.shape[0], sampleoutnorm.shape[1])  # 数据扩增
sampleoutnorm += noise

# 超参数
maxepochs = 70000  # 最大迭代次数
learning_rate = 0.035  # 学习率
errorfinal = 0.65 * 10 * (-3)  # 最低损失值
samnum = 20  # 样本数
indim = 3  # 输入特征数
outdim = 2  # 输出特征数
hiddenunitnum = 8  # 隐藏层神经元个数

# 网络设计
w1 = 0.5 * np.random.rand(hiddenunitnum, indim)
b1 = 0.5 * np.random.rand(hiddenunitnum, 1)
w2 = 0.5 * np.random.rand(outdim, hiddenunitnum)
b2 = 0.5 * np.random.rand(outdim, 1)


# Sigmod激活函数
def logsig(x):
    return 1 / (1 + np.exp(-x))


# BP神经网络构建
def bp_net(sampleinnorm):
    global w1
    global w2
    global b1
    global b2

    # FP过程
    hiddenout = logsig((np.dot(w1, sampleinnorm) + b1))
    # 输出层输出
    networkout = np.dot(w2, hiddenout) + b2

    # 错误
    err = sampleoutnorm - networkout

    # BP过程
    delta2 = err
    delta1 = np.dot(w2.transpose(), delta2) * hiddenout * (1 - hiddenout)

    dw2 = np.dot(delta2, hiddenout.transpose())
    db2 = np.dot(delta2, np.ones((samnum, 1)))
    dw1 = np.dot(delta1, sampleinnorm.transpose())
    db1 = np.dot(delta1, np.ones((samnum, 1)))

    w2 += learning_rate * dw2
    b2 += learning_rate * db2

    w1 += learning_rate * dw1
    b1 += learning_rate * db1

    return networkout, err


errhistory = []
# BP算法遍历
for i in range(maxepochs):
    # 调用BP神经网络
    _, err = bp_net(sampleinnorm)
    sse = sum(sum(err ** 2))

    errhistory.append(sse)
    if sse < errorfinal:
        break

# 误差曲线图
errhistory10 = np.log10(errhistory)  # 为了更好的呈现损失数值,缩减数值
minerr = min(errhistory10)  # 取到最低损失
plt.plot(errhistory10)  # 呈现误差曲线
plt.plot(range(0, len(errhistory10)), [minerr] * len(range(0, len(errhistory10))))  # 最低损失
# 获取当前图表
ax = plt.gca()
# 设置Y轴数值
ax.set_yticks([-2, -1, 0, 1, 2, minerr])
# 设置Y轴刻度名
ax.set_yticklabels([u'$10^{-2}$', u'$10^{-1}$', u'$1$', u'$10^{1}$', u'$10^{2}$', str(('%.4f' % np.power(10, minerr)))])
# 设置X轴描述
ax.set_xlabel('iteration')
# 设置Y轴描述
ax.set_ylabel('error')
# 设置标题
ax.set_title('Error History')

# 呈现视图
plt.show()


# 不愿标准化
def de_max_min_norm(data, sampleoutminmax):
    # max-min
    diff = sampleoutminmax[1] - sampleoutminmax[0]
    # data * (max - min) + min
    data2 = data * diff + sampleoutminmax[0]
    return data2


# 仿真输出和实际输出对比图
# 仿真
networkout, _ = bp_net(sampleinnorm)
# 还原标准化
networkout2 = de_max_min_norm(networkout, sampleoutminmax)

# 真实值
sampleout = np.array(sampleout)

# 建立一个2 * 1的画布
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

# 1. 公路客运量
# 预测值,黑色圆点线段
line1, = axes[0].plot(networkout2[0], 'k', marker=u'$\circ$')
# 真实值,红色蓝色星星线段,星星大小9
line2, = axes[0].plot(sampleout[0], 'r', markeredgecolor='b', marker=u'$\star$', markersize=9)

# 标题设置,标签左上角,载入线段
axes[0].legend((line1, line2), ('simulation output', 'real output'), loc='upper left')

# Y轴坐标刻度
yticks = [0, 20000, 40000, 60000]
# Y轴坐标刻度名
ytickslabel = [u'$0$', u'$2$', u'$6$']
axes[0].set_yticks(yticks)
axes[0].set_yticklabels(ytickslabel)

# Y轴描述
axes[0].set_ylabel(u'passenger traffic$(10%4)$')

# X轴范围
xticks = range(0, 20, 2)
xtickslabel = range(1990, 2010, 2)
axes[0].set_xticks(xticks)
axes[0].set_xticklabels(xtickslabel)
axes[0].set_xlabel(u'year')
axes[0].set_title('Passenger Traffic Simulation')

# 2. 公路货运量
line3, = axes[1].plot(networkout2[1], 'k', marker=u'$\circ$')
line4, = axes[1].plot(sampleout[1], 'r', markeredgecolor='b', marker=u'$\star$', markersize=9)
axes[1].legend((line3, line4), ('simulation output', 'real output'), loc='upper left')
yticks = [0, 10000, 20000, 30000]
ytickslabel = [u'$0$', u'$1$', u'$2$', u'$3$']
axes[1].set_yticks(yticks)
axes[1].set_yticklabels(ytickslabel)
axes[1].set_ylabel(u'freight traffic$(10^4)$')

xticks = range(0, 20, 2)
xtickslabel = range(1990, 2010, 2)
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(xtickslabel)
axes[1].set_xlabel(u'year')
axes[1].set_title('Freight Traffic Simulation')

plt.show()
