#TensorFlow实现线性回归
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# 1.模拟数据
## 1.1 随机生成1000个点,围绕着y = 0.1 * x + 0.4的直线范围
vectors_sets = []
for _ in range(1000):
    # 均值为0.0, 方差为0.55的高斯分布随机数
    x1 = np.random.normal(loc=0.0, scale=0.55)
    # 构建出y的值,给原始数据增加噪声,从而符合真实数据的分布
    y1 = 0.1 * x1 + 0.4 + np.random.normal(0.0, 0.01)
    vectors_sets.append((x1, y1))

# 分割数据得到x和y
x_data = [v[0] for v in vectors_sets]
y_data = [v[1] for v in vectors_sets]

# 2.数据可视化
plt.scatter(x_data, y_data, c='r')
plt.plot(x_data, [0.1 * x + 0.4 for x in x_data])
plt.show()

# 3. 构建模型
# 3.1 建立超参数
hidden_size = 1
learning_rate = 0.5
# 3.2 建立输入数据和标签的占位符
x_input = tf.placeholder(tf.float32, shape=[len(x_data)])
y_label = tf.placeholder(tf.float32, shape=[len(y_data)])

# 3.3 构建结构
def net():
    # 1. 构建y = w * x + b的方程
    # 设置w和b两个变量
    W = tf.Variable(tf.random_uniform(shape=[hidden_size], minval=-1.0, maxval=1.0), name='W')
    B = tf.Variable(tf.zeros(shape=[hidden_size]), name='B')
    # 构建公式
    y = W * x_input + B
    return y, W, B


# 3.4 计算损失
y_, W, B = net()

# 均方差
loss = tf.reduce_mean(tf.square(y_ - y_label))

# 3.5 构建优化器进行损失的优化
# 采用梯度下降法来优化参数,训练的过程就是最小化误差值loss
train_op = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)
# minimize中有两部分,第一部分为计算梯度,第二部分为梯度应用到变量中,变量更新梯度值.

# 4. 训练模型
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(500):
        weight, bias, _, cost = sess.run([W, B, train_op, loss], feed_dict={x_input:x_data, y_label:y_data})
        print('W = {}, B = {}, Loss = {}'.format(weight, bias, cost))

    # 模型预测及可视化呈现
    plt.scatter(x_data, y_data, c='r')
    plt.plot(x_data, [sess.run(W) * x + sess.run(B) for x in x_data])
    plt.show()

# TensorFlow开发的一般流程
# 1. 准备数据,进行数据清洗以及预处理
# 2. 构建模型,返回模型预测值
# 3. 预测值和真实值计算损失
# 4. 优化器设置学习率优化损失
# 5. 迭代训练优化器
# 6. 可以根据准确率作为评估指标,或者反独促统模型,搭建可视化模型结构
# 7. 调用模型进行预测
