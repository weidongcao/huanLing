# coding=utf-8


import tensorflow as tf
import numpy as np
import argparse
import flask
from types import MethodType, FunctionType


class Config:
    def __init__(self):
        self.batch_size = 200
        self.epoches = 1000
        self.lr = 1e-5
        self.keep_prob = 0.7
        self.saves = 100
        self.prints_per_epoch = 2
        self.save_path = './model/'

        self.new_model = False
        self.start = False

    def __repr__(self):
        result = ''
        for name in dir(self):
            if name.startswith('__'):
                continue
            attr = getattr(self, name)
            if isinstance(attr, MethodType) or isinstance(attr, FunctionType):
                continue
            result += '%s: %s, ' % (name, attr)
        return result

    def __str__(self):
        return self.__repr__()

    def from_cmd_line(self):
        parser = argparse.ArgumentParser()
        for name in dir(self):
            if name.startswith('__'):
                continue
            attr = getattr(self, name)
            if isinstance(attr, MethodType) or isinstance(attr, FunctionType):
                continue
            if type(attr) == bool:
                parser.add_argument('--' + name, default=attr, action='store_true')
            else:
                parser.add_argument('--' + name, type=type(attr), default=attr)
        a = parser.parse_args()
        for name in dir(self):
            if name.startswith('__'):
                continue
            attr = getattr(self, name)
            if isinstance(attr, MethodType) or isinstance(attr, FunctionType):
                continue
            setattr(self, name, getattr(a, name))


class App:
    def __init__(self, tensors_fun, config: Config):
        graph = tf.Graph()
        with graph.as_default():
            self.tensors = tensors_fun()
            conf = tf.ConfigProto(allow_soft_placement=True)
            conf.gpu_options.allow_growth = True
            self.session = tf.Session(config=conf, graph=graph)
            self.saver = tf.train.Saver()
            if config.new_model:
                self.session.run(tf.global_variables_initializer())
                print('Use a new model from %s.' % config.save_path, flush=True)
            else:
                try:
                    self.saver.restore(self.session, config.save_path)
                    print('Restore model from %s success!' % config.save_path, flush=True)
                except:
                    self.session.run(tf.global_variables_initializer())
                    print('Fail to restore the model from %s, use a new model instead.' % config.save_path, flush=True)


if __name__ == '__main__':
    conf = Config()
    conf.from_cmd_line()
    print(conf)
    print(str(conf))
