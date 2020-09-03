# LeNet实现手写数字识别
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
    'wc1': tf.Variable(tf.random_normal([5, 5, 1, 20])),
    'wc2': tf.Variable(tf.random_normal([5, 5, 20, 50])),
    'wf1': tf.Variable(tf.random_normal([50 * 4 * 4, 500])),
    'out': tf.Variable(tf.random_normal([500, n_classes]))
}
bias = {
    'bc1': tf.Variable(tf.random_normal([20])),
    'bc2': tf.Variable(tf.random_normal([50])),
    'bf1': tf.Variable(tf.random_normal([500])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}


def net():
    #
    input_layer = tf.reshape(x, [-1, 28, 28, 1])

    # conv_1
    # filter 卷积核
    # strides 卷积核的步长 [batch_size, 'height'width' deep]
    # padding 边缘填充 VALID 向下取整
    with tf.name_scope('conv1'):
        # f(xw+b)
        conv1_layer_conv = tf.nn.conv2d(input=input_layer, filter=weights['wc1'], strides=[1, 1, 1, 1], padding='VALID')
        # bias_add 一个特殊的add'把bias均匀回到最后一个维度中
        conv1_layer_relu = tf.nn.relu(tf.nn.bias_add(conv1_layer_conv, bias['bc1']))
        # ksize 池化窗口大小 '[batch_size, height, width, Deep]
        # strides 池化的步长 [batch_size, height, width, Deep]
        # padding边缘填充 VALID 向下取整 SAME 向上取整
        conv1_layer_pool = tf.nn.max_pool(value=conv1_layer_relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                                          padding='VALID')

        with tf.name_scope('conv2'):
            conv2_layer_conv = tf.nn.conv2d(input=conv1_layer_pool, filter=weights['wc2'], strides=[1, 1, 1, 1],
                                            padding='VALID')
            # bias_add一个特殊的add,把bias远远回到最后一个维度中
            conv2_layer_relu = tf.nn.relu(tf.nn.bias_add(conv2_layer_conv, bias['bc2']))

            conv2_layer_pool = tf.nn.max_pool(value=conv2_layer_relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
                                              padding='VALID')

        with tf.name_scope('flatten'):
            # 4dim --> 2dim 为了fc能进行计算
            flatten_shape = conv2_layer_pool.get_shape()
            flatten = tf.reshape(conv2_layer_pool, [-1, flatten_shape[1] * flatten_shape[2] * flatten_shape[3]])

        with tf.name_scope('fc'):
            fc1 = tf.nn.sigmoid(tf.add(tf.matmul(flatten, weights['wf1']), bias['bf1']))

        with tf.name_scope('out'):
            return tf.add(tf.matmul(fc1, weights['out']), bias['out'])


pred = net()
print(pred)
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
train_epochs = 10000  # 迭代次数
batch_size = 100  # 每次处理图片数
display_step = 10  # 每十次进行评估,并调整学习率
lr = 0.001
saver = tf.train.Saver()
for step in range(train_epochs):
    # 取出批量数据
    batch_total = mnist.train.num_examples // batch_size
    for i in range(batch_total):
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        sess.run(optm, feed_dict={x: batch_x, y: batch_y, learning_rate: lr})
    if step % display_step == 0:
        batch_test_x, batch_test_y = mnist.test.next_batch(batch_size)
        batch_train_x, batch_train_y = mnist.train.next_batch(batch_size)
        train_acc, train_loss = sess.run([accr, cost], feed_dict={x: batch_train_x, y: batch_train_y})
        test_acc, test_loss = sess.run([accr, cost], feed_dict={x: batch_test_x, y: batch_test_y})
        print('Step:{}, train_loss:{}, test_loss:{}, train_acc:{}, test_acc:{}'.format(step, train_loss, test_loss,
                                                                                       train_acc, test_acc))
        lr *= 0.8

        if train_acc > 0.9 and test_acc > 0.9:
            saver.save(sess, 'model/bp_mnist', step)
            break
writer = tf.summary.FileWriter('log', sess.graph)
writer.close()
