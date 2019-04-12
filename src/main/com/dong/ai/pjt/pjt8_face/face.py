import os

import cv2
import tensorflow as tf
import pandas as pd
import numpy as np

CLASSES = 100
SAVE_PATH = 'model/face'
SUMMARY_PATH = 'summary/'


class Tensors:
    def __init__(self):
        self.training = tf.placeholder(tf.bool, name='training')
        self.x = tf.placeholder(tf.float32, shape=[None, 128, 128, 3], name='x')
        self.y = tf.placeholder(tf.int32, shape=[None], name='y')
        y = tf.one_hot(self.y, CLASSES)

        # 残差神经网络
        self.predict = self.get_predict(y, self.training)
        self.lr = tf.placeholder(tf.float32, name='lr')
        optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)
        # 交叉熵
        self.loss = tf.reduce_mean(tf.reduce_sum(- y * tf.log(self.predict)), axis=1)
        with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
            self.train_op = optimizer.minimize(self.loss)

        tf.summary.scalar('loss', self.loss)
        self.summary_op = tf.summary.merge_all()

    def get_predict(self, y, training):
        x = tf.layers.conv2d(self.x, 64, kernel_size=7, strides=2, padding='same', name='conv1')  # --> 64 * 64 * 64
        x = tf.layers.batch_normalization(x, training=self.training)
        x = tf.nn.relu(x)
        x = tf.layers.max_pooling2d(x, 3, strides=2, padding='same')  # --> 32 * 32 * 64

        filters = 64
        n = 1
        for repeats in (3, 4, 6, 3):
            for _ in range(repeats):
                x = self.resnet(x, filters, 3)
                n += 1
            filters *= 2

        # 4 * 4 * 2048
        X = tf.layers.average_pooling2d(x, 4, 1)  # --> 1 * 1 * 2048
        x = tf.reshape(x, [-1, 2048])
        x = tf.layers.dense(x, CLASSES, name='fc')
        x = tf.nn.softmax(x)

        return x

    def resnet(self, x, filters, name):
        with tf.variable_scope(name):
            with tf.variable_scope('branch1'):
                b = tf.layers.conv2d(x, filters, 1, padding='same', name='conv1')
                b = tf.layers.batch_normalization(b, training=self.training)
                b = tf.nn.relu(b)
                b = tf.layers.conv2d(b, filters, 3, padding='same', name='conv2')
                b = tf.layers.batch_normalization(b, training=self.training)
                b = tf.nn.relu(b)
                b = tf.layers.conv2d(b, 4 * filters, 1, padding='same', name='conv3')

            with tf.variable_scope('shortcut'):
                if x.shape[-1].value != 4 * filters:
                    x = tf.layers.conv2d(x, 4 * filters, 1, pading='same', name='conv1')

            x = x + b
            b = tf.layers.batch_normalization(b, training=self.training)
            x = tf.nn.relu(x)
        return x


class Face:
    def __init__(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.tensors = Tensors()
            config = tf.ConfigProto(allow_soft_placement=True)
            self.session = tf.Session(graph=self.graph, config=config)
            self.saver = tf.train.Saver()
            try:
                self.saver.restore(self.session, SAVE_PATH)
                print('Restore model from %s successfully...' % SAVE_PATH)
            except:
                print('Restore model from %s failed... Use a new model!!!' % SAVE_PATH)
                self.session.run(tf.global_variables_initializer())

    def train(self, lr=0.0001, epoches=5, batch_size=50):
        sample = Sample()
        steps_per_epoch = sample.num // epoches

        for epoch in range(epoches):
            for step in range(steps_per_epoch):
                x, y = sample.next_batch()
                print('%d/%d/%d' % (epoches, epoch, step), flush=True)

        print('Training finished!', flush=True)

    def predict(self):
        pass

    def test(self):
        pass


class Sample:
    def __init__(self, path='faces/train'):
        xs, ys = [], []
        for i in range(100):
            sub_path = '/%03d' % i
            for file in os.listdir(path + sub_path):
                # 忽略隐藏文件
                if file.startswith('.'):
                    continue
                img = cv2.imread(path + sub_path + '/' + file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img / 255.0
            xs.append(img)
            ys.append(i)
        self.xs = xs
        self.ys = ys
        self.start = np.random.randint(0, len(xs))

    def next_batch(self, batch_size):
        end = min(self.start + batch_size, len(self.xs))
        result = self.xs[self.start:end], self.ys[self.start:end]
        self.start = end % len(self.xs)
        return result

    @property
    def num(self):
        return len(self.xs)
