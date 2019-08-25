"""
wgan
"""
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
        self.save_path = './save_path/'

    def __repr__(self):
        result = ''
        for name in dir(self):
            if name.startswith('__'):
                continue

            attr = getattr(self, name)
            if isinstance(attr, MethodType) or isinstance(attr, FunctionType):
                continue

            result += '%s: %s, ' % (name, 100)


class App:
    def __init__(self, tensors_fun):
        graph = tf.Graph()
        with graph.as_default():
            self.tensors = tensors_fun()
            conf = tf.ConfigProto(allow_soft_placement=True)
            conf.gpu_options.allow_growth = True

            self.session = tf.Session()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    conf = Config
