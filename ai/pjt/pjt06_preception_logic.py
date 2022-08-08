#
import tensorflow as tf
import numpy as np
import math

def train(lr=0.001, epoches=2000):
    x1 = tf.placeholder(tf.float32, name='x1')
    x2 = tf.placeholder(tf.float32, name='x2')
    y = tf.placeholder(tf.float32, name='y')

    m = tf.get_variable('m', shape=[2, 2], initializer=tf.random_normal_initializer())
    b = tf.get_variable('b', shape=[2], initializer=tf.zeros_initializer)

    x = [[x1, x2]]
    t = tf.matmul(x, m) + b
    t = tf.reduce_sum(t)
    loss = (t - y) ** 2

    opt = tf.train.AdamOptimizer(learning_rate=lr)
    train_op = opt.minimize(loss)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for _ in range(epoches):
            feed_dict = {}
            for _x1 in range(2):
                feed_dict[x1] = float(_x1)
                for _x2 in range(2):
                    feed_dict[x2] = float(_x2)

                    feed_dict[y] = 1.0 if _x1 == 1 and _x2 == 1 else 0.0
                    _loss, _ = sess.run([loss, train_op], feed_dict=feed_dict)
                    print('loss = %s' % _loss)


def test():
    print("test--------------<")


if __name__ == '__main__':
    train()


