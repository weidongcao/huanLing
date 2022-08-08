# 手写数字识别
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

SAVE_PATH = 'model/mnist'
SUMMAY_PATH = 'summary/'
# 定义一个磁盘路径,存放监视数据
# 把所有的监视数据用summary_all,
# 在train中定义一个File_Writer
# Session.run
# 打开Tensorboard进行监视
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
        x = tf.layers.max_pooling2d(x, 2, 2, padding='same')

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
        self.predict = tf.nn.softmax(x)

        tf.summary.scalar('loss', loss)
        self.summary_op = tf.summary.merge_all()


class Mnist:
    def __init__(self):
        graph = tf.Graph()
        self.graph = graph
        with graph.as_default():
            self.tensors = Tensors()
            self.session = tf.Session(graph=graph)
            self.saver = tf.train.Saver()
            try:
                self.saver.restore(self.session, SAVE_PATH)
                print('Restore the model from %s successfully...' % SAVE_PATH)
            except:
                print('Fail to restore the model from %s, use a new model instead' % SAVE_PATH)
            self.session.run(tf.global_variables_initializer())

    def train(self, batch_size=64, epoches=5, lr=0.0002):
        ds = input_data.read_data_sets('data/')
        num = ds.train.num_examples
        step_per_epoch = num // batch_size

        file_writer = tf.summary.FileWriter(SUMMAY_PATH, graph=self.graph)
        for epoch in range(epoches):
            for step in range(step_per_epoch):
                imgs, labels = ds.train.next_batch(batch_size)
                feed_dict = {
                    self.tensors.x: imgs,
                    self.tensors.y: labels,
                    self.tensors.lr: lr
                }
                _, loss, summary = self.session.run(
                    [
                        self.tensors.train_op,
                        self.tensors.loss,
                        self.tensors.summary_op
                    ],
                    feed_dict
                )
                file_writer.add_summary(summary, epoch * step_per_epoch + step)
                print("%d / %d, %d / %d: loss = %s" % (step, step_per_epoch, epoch, epoches, loss))
            self.saver.save(self.session, SAVE_PATH)
            print('model saved into %s' % SAVE_PATH)

        self.saver.save(self.session, SAVE_PATH)
        print('model saved into %s' % SAVE_PATH)
        self.session.close()

    def predict(self, batch_size=64):
        ds = input_data.read_data_sets('data/')
        num = ds.test.num_examples
        steps = num // batch_size
        precise, n = 0.0, 0
        for step in range(steps):
            imgs, labels = ds.test.next_batch(batch_size)
            feed_dict = {
                self.tensors.x: imgs
            }
            pred = self.session.run(self.tensors.predict, feed_dict)
            pred = np.argmax(pred, axis=1)
            precise += np.mean(np.float32(np.equal(pred, labels)))

            n += 1
        print('precise: %s' % (precise / n))


if __name__ == '__main__':
    mnist = Mnist()
    mnist.train()
    # mnist.predict()
