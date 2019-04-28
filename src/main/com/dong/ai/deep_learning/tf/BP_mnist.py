# 使用BP神经网络实现手写数字识别

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 引入数据
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

# 超参数
learning_rate = tf.placeholder(tf.float32)
in_dim = 784
n_classes = 10
hidden_size_1 = 256
hidden_size_2 = 128

# 数据占位符
x = tf.placeholder(tf.float32, [None, in_dim])
y = tf.placeholder(tf.float32, [None, n_classes])

# 设置权重和偏置量

weights = {
    'w1': tf.Variable(tf.random_normal([in_dim, hidden_size_1], stddev=0.1)),
    'w2': tf.Variable(tf.random_normal([hidden_size_1, hidden_size_2], stddev=0.1)),
    'w_out': tf.Variable(tf.random_normal([hidden_size_2, n_classes], stddev=0.1))
}
bias = {
    'b1': tf.Variable(tf.random_normal([hidden_size_1], stddev=0.1)),
    'b2': tf.Variable(tf.random_normal([hidden_size_2], stddev=0.1)),
    'b_out': tf.Variable(tf.random_normal([n_classes], stddev=0.1))
}


def net():
    # 第一个隐藏层
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['w1']), bias['b1']))
    # 第二个隐藏层
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['w2']), bias['b2']))
    # 输出层
    return tf.add(tf.matmul(layer_2, weights['w_out']), bias['b_out'])


pred = net()
# loss
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
# 准确率
corr = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accr = tf.reduce_mean(tf.cast(corr, tf.float32))

# 优化器
optm = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# 训练
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# 参数
training_epochs = 1000  # 迭代次数
batch_size = 100  # 每次处理图片数
display_step = 10  # 每10次进行一次评估,并调整学习率
lr = 0.001
saver = tf.train.Saver()

for step in range(training_epochs):
    # 取出指数据
    batch_total = mnist.train.num_examples // batch_size
    for i in range(batch_total):
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        sess.run(optm, feed_dict={x: batch_x, y: batch_y, learning_rate: lr})
    if step % display_step == 0:
        batch_test_x, batch_test_y = mnist.test.next_batch(batch_size)
        batch_train_x, batch_train_y = mnist.train.next_batch(batch_size)
        train_acc, train_loss = sess.run([accr, cost], feed_dict={x: batch_test_x, y: batch_test_y})
        test_acc, test_loss = sess.run([accr, cost], feed_dict={x: batch_test_x, y: batch_test_y})
        print('Step:{}, train_loss:{}, test_loss:{}, train_acc:{}, test_acc:{}'.format(step, train_loss, test_loss,
                                                                                       train_acc, test_acc))

        lr *= 0.8

        if train_acc > 0.9 and test_acc > 0.9:
            saver.save(sess, 'model/bp_mnist', step)
            break
writer = tf.summary.FileWriter('log', sess.graph)
writer.close()
