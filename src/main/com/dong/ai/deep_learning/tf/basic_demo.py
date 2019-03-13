import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 首先,创建一个TensorFlow常量 --> 2
const = tf.constant(2.0, name='const')


# TensorFlow中,使用tf.constant()定义常量,使用tf.Variable()定义变量.TensorFlow可以自动进行数据类型检测,
# 比如:赋值2.0就默认为tf.float32,但是最好还是地定义
# 创建TensorFlow变量b和c
#b = tf.Variable(2.0, name='b')
c = tf.Variable(1.0, dtype=tf.float32, name='c')

# 定义运算符(也称为TensorFlow Operation)


# TensorFlow中所有的变量必须经过初始化才能使用,初始化方式分两步:
#     1. 案底初始化Operation
#     2. 运行初始化Operation
# 1. 定义init Operation
init_op = tf.global_variables_initializer()

# 运行Graph需要先调用 tf.Session()函数创建一个会话(Session).Session就是我们与Graph交互的Handle.
#Session
#with tf.Session() as sess:
    # 2. 运行init operation
    #sess.run(init_op)
    # 计算
    #a_out = sess.run(a)
    #print("Variable a is {}".format(a_out))

# The TensorFlow placeholder
# 对于上面的例子的改进:使变量f可以接收任意值.TensorFlow中接收值的方式为占位符(placeholder),
# 通过tf.placeholder()创建
# 创建placeholder
b = tf.placeholder(tf.float32, [None, 1], name='b')
d = tf.add(b, c, name='d')
e = tf.add(c, const, name='3')
a = tf.multiply(d, e, name='a')
# 第二个参数值为[None, 1],其中None表示不确定,即不确定第一个维度的大小,第一维可以是任意大小,
# 特别对应tensor数量(或者样本数量),输入的tensor数目可以是32, 64

# 如果要得到计算结果,需要在运行过程中feed占位符,具体为将a_out = sess.run(a)改为:
# a_out = sess.run(a, feed_dict={b:np.arange(0, 10)[:, np.newaxis]})

with tf.Session() as sess:
    sess.run(init_op)
    a_out = sess.run(a, feed_dict={b: np.arange(0, 10)[:, np.newaxis]})

    print("Variable a is {}".format(a_out))

# 神经网络的例子,数据集为MNIST数据集
# 加载数据
# ont_hot=True表示对label进行one-hot编码,比如标签4可以表示为[0,0,0,0,1,0,0,0,0,0].
# 这是神经网络输出层要求的格式
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# 定义超参数和placeholder
# 超参数
learning_rate = 0.5
epochs = 10
batch_size=100

#placeholder
# 输入图片为28 * 28像素 = 784
x = tf.placeholder(tf.float32, [None, 784])
# 输出为0-9的one-hot编码(再次强调,[None,784]中的None表示任意值,特别对应tensor数目)
y = tf.placeholder(tf.float32, [None, 10])

# 定义参数w和b
# hidden layer => w, b
W1 = tf.Variable(tf.random_normal([784, 300], stddev=0.03), name='W1')
b1 = tf.Variable(tf.random_normal([300]), name='b1')

#output layer => w,b
W2 = tf.Variable(tf.random_normal([300, 10], stddev=0.03), name='W2')
b2 = tf.Variable(tf.random_normal([10]), name='b2')
# 在这里,要了解全连接层的两个参数w和b都是需要随机初始化的,tf.random_normal()生成正态分布的随机数

# 构造隐藏层网络
#hidden layer
hidden_out = tf.add(tf.matmul(x, W1), b1)
hidden_out = tf.nn.relu(hidden_out)

# 构造输出(预测值)
# 计算输出
y_ = tf.nn.softmax(tf.add(tf.matmul(hidden_out, W2), b2))

# BP部分-定义loss
y_clipped = tf.clip_by_value(y_, 1e-10, 0.9999999)
with tf.name_scope('Loss'):
    loss = -tf.reduce_mean(tf.reduce_sum(y * tf.log(y_clipped) + (1 - y) * tf.log(1 - y_clipped), axis=1))

# BP部分-定义优化算法
# 创建优化器,确定优化目标
# optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimizer(cross_entropy)
# optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimizer(cross_entropy)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)
# 定义初始化operation和准确率node

# 创建准确率节点
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
with tf.name_scope('Accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

tf.summary.scalar('Loss', loss)
tf.summary.scalar('Accuracy', accuracy)

init = tf.global_variables_initializer()
merged_summary_op = tf.summary.merge_all()

# 开始训练
# 创Session
with tf.Session() as sess:
    sess.run(init)
    total_batch = int(len(mnist.train.labels) / batch_size)
    for epoch in range(epochs):
        avg_cost = 0
        for i in range(total_batch):
            batch_x, batch_y = mnist.train.next_batch(batch_size=batch_size)
            _, c = sess.run([optimizer, loss], feed_dict={x: batch_x, y: batch_y})

            avg_cost += c / total_batch
        print("Epoch:" , (epoch + 1), "cost = ", "{:.3f}".format(avg_cost))


        loss_, acc = sess.run([loss, accuracy], feed_dict={x:batch_x, y:batch_y})
        print("epoch{}, lost{:.4f}, acc {:.3f}".format(epoch, loss_, acc))
        print()


    # print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))

