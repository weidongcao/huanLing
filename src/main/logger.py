# -*- coding: utf-8 -*-
# @Time    : 2020-08-15 22:38
# @Author  : CaoWeidong
# @Email   : caowd1990@163.com
# @File    : logger.py
# @Software: IntelliJ IDEA

import logging.config
import os

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logger.ini'))
logger = logging.getLogger("root")
