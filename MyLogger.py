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
    def get_logger(self, name="root"):
        logging.config.fileConfig("logger.ini")
        # logging.config.fileConfig(self.file)
        return logging.getLogger(name)


logger = Logger().get_logger()
logger.info("w ksks lkslksjdflskdjfj")
