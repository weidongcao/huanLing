import os

import cv2
import numpy as np
import tensorflow as tf

CLASSES = 100
SAVE_PATH = 'model/face'
SUMMARY_PATH = 'summary/'


class Tensors:
    def __init__(self, gpus):

        self.training = tf.placeholder(tf.bool, name='training')
        self.lr = tf.placeholder(tf.float32, name='lr')
        optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)

        self.x_s = []
        self.y_s = []
        self.predict_s = []
        self.loss_s = []

        for gpu_id in range(gpus):
            x = tf.placeholder(tf.float32, shape=[None, 128, 128, 3], name='x')
            y = tf.placeholder(tf.int32, shape=[None], name='y')
            self.x_s.append(x)
            self.y_s.append(y)
            y = tf.one_hot(self.y, CLASSES)

            # 残差神经网络
            predict = self.get_predict(y)
            self.predict_s.append(predict)

            # 交叉熵
            loss = tf.reduce_mean(tf.reduce_sum(- y * tf.log(predict)), axis=1)
            self.loss_s.append(loss)

            self.grad_s.append(optimizer.compute_gradients(loss))
            tf.get_variable_scope().reuse_variables()

        tf.get_variable_scope()._reuse = tf.AUTO_REUSE
        with tf.device('/gpu:0'):
            vg_dict = self.get_vg_dict()
            g_v_list = self.get_g_v_list(vg_dict)
            with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
                self.train_op = optimizer.apply_gradients(g_v_list)

        loss = tf.reduce_mean(self.loss_s)
        tf.summary.scalar('loss', self.loss)
        self.summary_op = tf.summary.merge_all()

    def get_vg_dict(self):
        result = {}
        for vgs in self.grad_s:
            for g, v in vgs:
                if not v in result:
                    result[v] = []
                result[v].append(g)
        return result

    def get_g_v_list(self, vg_dict):
        return [(tf.reduce_mean(vg_dict[v], axis=0), v) for v in vg_dict]

    def get_predict(self, x):
        x = tf.layers.conv2d(x, 64, kernel_size=7, strides=2, padding='same', name='conv1')  # --> 64 * 64 * 64
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


def get_gpus():
    value = os.getenv('CUDA_VISIBLE_DEVICES', '0')
    return len(value.split(','))


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
        self.should_stop = False

    def stop(self):
        self.should_stop = True

    def train(self, lr=0.0001, epoches=5, batch_size=50):
        self.lr = lr
        self.epoches = epoches
        self.batch_size = batch_size

        # file_writer =
        sample = Sample()
        steps_per_epoch = sample.num // epoches

        for epoch in range(epoches):
            if self.should_stop:
                break

            for step in range(steps_per_epoch):
                if self.should_stop:
                    break
                feed_dict = {
                    self.tensors.lr: self.lr,
                    self.tensors.training: True,
                }
                for gpu_id in range(get_gpus()):
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


import flask

app = flask.Flask()
face = None

@app.route('/train')
def train():
    return False

if __name__ == '__main__':
    face = Face()
    face.train()