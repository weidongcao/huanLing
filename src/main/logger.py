# -*- coding: utf-8 -*-
# @Time    : 2020-08-15 22:38
# @Author  : CaoWeidong
# @Email   : caowd1990@163.com
# @File    : logger.py
# @Software: IntelliJ IDEA

import logging.config
import os

import yaml

__author__ = "caoweidong"


class Logger(object):
    def __init__(self):
        # self.file = 'resources/logger.conf'
        parent = os.path.dirname(os.path.realpath(__file__))
        self.file = os.path.join(parent, 'resources/config.yaml')

    def get_logger(self, name="root"):
        with open( self.file, 'r', encoding='utf-8') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(conf)
        # logging.config.fileConfig(self.file)
        return logging.getLogger(name)


logger = Logger().get_logger()
logger.info("aaa")
