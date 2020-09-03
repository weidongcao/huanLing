# 通过mnist项目测试TensorFlow的可视化

# 未来函数,主要用于兼容python2
# 引入绝对路径
from __future__ import absolute_import
# 除法
# 比如在python2中 1 / 2 = 0
# 在python3中 1 / 2  = 0.5
from __future__ import division
# print输出函数
# python2中print 1
# python3中print(1)
from __future__ import print_function

import argparse
import os
import sys

import tensorflow as tf

# TensorFlow提供的官方的训练数据包
from tensorflow.examples.tutorials.mnist import input_data

# 一开始先把所有内容清空,防止没有得到数据
FLAGS = None


def train():
    # 读取数据
    # mnist类,到TensorFlow1.8之后就变了,此程序最好不要在TensorFlow1.8以上跑,会出问题的.
    # 将会返回4个变量,
    #   第一个变量为训练集的图片
    #   第二个变量为训练集的标签
    #   第三个变量为测试集的图片
    #   第四个变量为测试集的标签

    # FLAGS.data_dir:读取的数据放置的目录
    # fake_data:返回虚假数据,即噪音数据
    # one_hot:十分类的标签one_hot化,变为哑变量,
    # 即将十进制数据转为one_hot类型的数据,即长度为10,数字是几则第几位数字为1,其他全部为0
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True, fake_data=FLAGS.fake_data)

    # 交互式会话
    sess = tf.InteractiveSession()

    # 输入层
    with tf.name_scope('input'):
        x = tf.placeholder(tf.float32, [None, 784], name='x-input')
        y_ = tf.placeholder(tf.float32, [None, 10], name='y-input')

    with tf.name_scope('input_reshape'):
        # 转置为图片形式
        image_shaped_input = tf.reshape(x, [-1, 28, 28, 1])
        # Summary.image 记录图片,记录多少图片
        tf.summary.image('input', image_shaped_input, 10)

    # 生成权重变量
    # We can't initialize There Variables to 0 - the Network Will get stuck
    def weight_variable(shape):
        # 截断正态分布随机数
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    # 生成偏置量
    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    # 记录变量
    def variable_summaryies(var):
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(var)
            # scalar记录点
            tf.summary.scalar('mean', mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(var))
            tf.summary.scalar('min', tf.reduce_min(var))
            # histogram直方图
            tf.summary.histogram('histogram', var)

    # 网络层
    # input_tensor  层输入数据
    # input_dim  输入数据的特征数
    # output_dim 输出数据的特征数
    # layer_name 层名
    # act 激活函数
    def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu()):
        with tf.name_scope(layer_name):
            with tf.name_scope('weights'):
                weights = weight_variable([input_dim], output_dim)
                variable_summaryies(weights)
            with tf.name_scope('biases'):
                biases = bias_variable(['biases'])
                variable_summaryies(biases)
            with tf.name_scope('Wx_plus_b'):
                # w * x + b
                preactivate = tf.matmul(input_tensor, weights) + biases
                tf.summary.histogram('pre_activations', preactivate)
            # 神经元的输出普遍都需要激活,因此调用激活函数激活一下
            # 激活函数的目的是什么呢?
            #   给线性函数加入非线性的因素,这样才能进行拟合
            activations = act(preactivate, name='activation')
            tf.summary.histogram('activations', activations)
            return activations

    hidden1 = nn_layer(x, 784, 500, 'layer1')

    # dropout 处理过拟合,随机把某些神经元的输出置0
    # keep_prob表示保留神经元的比例
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)
        tf.summary.scalar('dropout_keep_rpobability', keep_prob)
        dropped = tf.nn.dropout(hidden1, keep_prob)

        # 输出层
        # tf.identity 不做任何处理
        # 其实也不是什么也不做,它在计算图内部创建了两个节点send 发送/recv接收
        y = nn_layer(dropped, 500, 10, 0, 'layer2', act=tf.identity)

        with tf.name_scope('cross_entropy'):
            # Softmax交叉熵损失函数
            # 先做一次Softmax然后做交叉熵损失函数
            diff = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logist=y)
            with tf.name_scope('total'):
                cross_entropy = tf.reduce_mean(diff)
        tf.summary.scalar('cross_entropy', cross_entropy)

        with tf.name_scope('train'):
            # 优化器梯度下降 Adam
            # 为什么使用Adam呢?
            #   因为一般交叉熵对应的优化器都会选择Adam
            # minimize 最小化损失,主要做了两步:计算梯度,更新参数)
            train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(cross_entropy)

        # 准确率
        # 使用argmax提取最大值所在的下标
        #
        with tf.name_scope('accuracy'):
            with tf.name_scope('correct_prediction'):
                # 等值判断,返回布尔矩阵
                correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
            with tf.name_scope('accuracy'):
                # cast数据类型转换
                accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        tf.summary.scalar('accuracy', accuracy)

    merged = tf.summary.merge_all()

    # 构建日志
    train_writer = tf.sumamry.FileWriter(FLAGS.log_dir + '/train', sess.graph)
    test_writer = tf.summary.FileWriter(FLAGS.log_dir + '/test')
    tf.global_variables_initializer().run()

    def feed_dict(train):
        if train or FLAGS.fake_data:
            xs, ys = mnist.train.next_batch(100, fake_data=FLAGS.fake_data)
            k = FLAGS.dropout
        else:
            xs, ys = mnist.test.images, mnist.test.labels
            k = 1.0
        return {x: xs, y_: ys, keep_prob: k}

    for i in range(FLAGS.max_steps):
        if i % 10 == 0:
            summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False))
            test_writer.add_summary(summary, i)
            print('Accuracy at step %s: %s' % (i, acc))
        else:
            # 运行状态,包括迭代次数,运行时间,当前时间
            if i % 100 == 99:
                run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                run_metadata = tf.RunMetadata()
                summary, _ = sess.run(
                    [merged, train_step],
                    feed_dict=feed_dict(True),
                    options=run_options,
                    run_metadata=run_metadata
                )

                train_writer.add_run_metadata(run_metadata, 'step % 03d' % i)
                train_writer.add_summary(summary, i)
                print('Adding run metadata for', i)
            else:
                summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
                train_writer.add_summary(summary, i)
            train_writer.close()
            test_writer.close()


def main(_):
    # 判断log文件路径是否存在
    # sys.path.exists
    if tf.gfile.Exists(FLAGS.log_dir):
        # 删除目录
        tf.gfile.DeleteRecursively(FLAGS.log_dir)

    # 构建目录
    tf.gfile.MakeDirs(FLAGS.log_dir)
    train()


## 运行
# In[]
# 命令行参数包 argparse
# python a.py --fake_data=True --learning_rate=0.1 --dropout=0.5
# python a.py --help
parser = argparse.ArgumentParser()
parser.add_argument('--fake_data', nargs='?', const=True, type=bool, default=False,
                    help='If true, uses fake data for unit testing.')
parser.add_argument('--max_steps', type=int, default=1000, help='Number of step to run trainer')
parser.add_argument('--learning_rate', type=float, default=0.001, help='Initial learning rate')
parser.add_argument('--dropout', type=float, default=0.9, help='Keep probability for training dropout.')
parser.add_argument('--data_dir', type=str, default=os.path.join(os.getenv('TEST_TMPDIR', 'tmp'), 'data'),
                    help='Directory for storing input data')
parser.add_argument('--log_dir', type=str,
                    default=os.path.join(os.getenv('TEST_TMPDIR', 'tmp'), 'mnist_with_summaries'),
                    help='Sumaries log directory')

# 获取命令传递过来的参数
# FLAGS parser
# unparsed 不在parser中传递的参数
FLAGS, unparsed = parser.parse_known_args()
tf.app.run(main=main, argv=[sys.argv[0] + unparsed])
