# -*- coding: utf-8 -*-
# @Time    : 2020-03-08 20:37:00
# @Author  : CaoWeidong
# @Email   : wd.cao@yamu.com
# @File    : logger_helper.py
# @Software: IntelliJ IDEA

import logging.config
import sys
from pathlib import Path, PurePath

# 如果程序入口不是模块根路径，调用logger会出问题，
# 比如说引入下面的这个import
# 需要先把根路径加入到Python环境路径
from helper.util import load_file, find_relative_path, get_dict_value_by_dot

cur_path = Path(__file__).parent.absolute()
root_path = cur_path.parent
sys.path.append(root_path.__str__())


logger_conf_filename = 'logger.yml'
main_conf_file = "config/engine-main.yml"
log_conf_item = "config.server.is_config_center"
all_logger = None

def get_logger_conf(conf_file_path=logger_conf_filename):
    """
    读取logging配置文件
    config/engine-main.yml为主配置
    config.server.is_config_center为配置项
    如果主配置文件及配置项存在则从apollo读取配置
    如果不存在则从本地读取配置
    :param conf_file_path:
    :return:
    """
    dt: dict = load_file(find_relative_path(main_conf_file))

    # 如果engine-main.yml主配置文件不存在默认读取本地配置文件
    # 如果engine-main.yml主配置文件不存在config.server.is_config_center配置项则默认读取本地配置文件
    if not dt or not get_dict_value_by_dot(dt, log_conf_item):
        conf_file_path = f"config/{conf_file_path}"
        logger_config_path = find_relative_path(Path(conf_file_path))
        lc: dict = load_file(logger_config_path.absolute().__str__())
    else:
        from helper.apollo_helper import apollo_helper
        lc: dict = apollo_helper.get_namespace(logger_conf_filename)

    return lc


def get_all_logger(name=None):
    """
    在不同的目录下执行,在不同的脚本下调用
    均可正确获取logging模块的配置文件
    :return:
    """
    logger_conf = get_logger_conf()
    handlers_conf: dict = logger_conf["handlers"]

    # create log path
    # reset log path
    for k in handlers_conf.keys():
        hc = handlers_conf[k]
        if "filename" in hc:
            log_path = Path(__file__).parent.parent.joinpath(PurePath(hc["filename"]))
            log_path.parent.mkdir(parents=True, exist_ok=True)
            logger_conf["handlers"][k]["filename"] = log_path.absolute().__str__()

    # 根据不同脚本打印不同格式的日志的问题暂时还没有解决,
    # 暂定所有脚本都使用root模块的格式
    # TODO
    # name = "root"
    # name_logger = logger.getLogger(name)

    # 后期可以配置打印彩色日志
    # TODO
    # coloredlogs.install(level=logging.DEBUG, logger=name_logger, reconfigure=False)

    logging.config.dictConfig(logger_conf)
    return True


def get_logger(name="root"):
    global all_logger
    if not all_logger:
        all_logger = get_all_logger()

    return logging.getLogger(name)


if __name__ == '__main__':
    logger1 = get_logger("root")
    logger2 = get_logger("module")
    logger3 = get_logger("module.x")
    logger4 = get_logger(__name__)
    logger1.debug("test helper logger")
    logger2.debug("test helper logger")
    logger3.debug("test helper logger")
    logger4.debug("test helper logger")
    logger1.info("test helper logger")
    logger2.info("test helper logger")
    logger3.info("test helper logger")
    logger1.warning("test helper logger")
    logger2.warning("test helper logger")
    logger3.warning("test helper logger")
    logger1.error("test helper logger")
    logger2.error("test helper logger")
    logger3.error("test helper logger")
    logger1.critical("test helper logger")
    logger2.critical("test helper logger")
    logger3.critical("test helper logger")
