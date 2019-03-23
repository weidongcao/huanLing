# 手写数字识别
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data


class Tensors:
    def __init__(self):
        x = tf.placeholder(tf.float32, [None, 28 * 28], name='x')
        y = tf.placeholder(tf.int32, [None], name='y')

        self.x = x
        self.y = y

        x = tf.reshape(x, [-1, 28, 28, 1])
        x = tf.layers.conv2d(x, 32, 3, padding='same')

        x = tf.nn.relu(x)
        x = tf.layers.max_pooling2d(x, 2, 2, padding='same')

        x = tf.layers.conv2d(x, 64, 3, padding='same')
        x = tf.nn.relu(x)
        x = tf.layers.max_pooling2d(x,2,2,padding='same')

        x = tf.reshape(x, [-1, 7 * 7 * 64])
        x = tf.layers.dense(x, 1000, activation=tf.nn.relu)

        x = tf.layers.dense(x, 10)

        loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=x, labels=y))
        lr = tf.placeholder(tf.float32, name='lr')
        optimizer = tf.train.AdamOptimizer(learning_rate=lr)
        train_op = optimizer.minimize(loss)
        self.loss = loss
        self.lr = lr
        self.train_op = train_op


class Mnist:
    def __init__(self):
        graph = tf.Graph()
        with graph.as_default():
            self.tensors = Tensors()
            self.session = tf.Session(graph=graph)
            self.session.run(tf.global_variables_initializer())


    def train(self, batch_size=64, epoches=5, lr=0.0002):
        ds = input_data.read_data_sets('data/')
        num = ds.train.num_examples
        step_per_epoch = num // batch_size

        for epoch in range(epoches):
            for step in range(step_per_epoch):
                imgs, labels = ds.train.next_batch(batch_size)
                feed_dict = {
                    self.tensors.x : imgs,
                    self.tensors.y : labels,
                    self.tensors.lr: lr
                }
                loss, _ = self.session.run([self.tensors.loss, self.tensors.train_op], feed_dict)
                print("%d / %d, %d / %d: loss = %s" % (step, step_per_epoch, epoch, epoches, loss))
        self.session.close()


if __name__ == '__main__':
    mnist = Mnist()
    mnist.train()
