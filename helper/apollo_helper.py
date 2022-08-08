# -*- coding:utf-8 -*-
from pathlib import Path

import yaml

from helper.util import get_dict_value_by_key_list, find_relative_path, load_file

class ApolloHelper:
    """
    python 连接 apollo配置中心工具类
    """

    def __init__(self, app_id, url="http://localhost:8080", secret='', cluster="default", read_apollo=False):
        """

        初始化apollo连接,
        同时将apollo配置同步到本地,
        以防止apollo服务挂了导致整个系统瘫痪

        :param app_id:
        :param secret:
        :param cluster:
        """
        self.url = url
        self.cluster = cluster
        self.app_id = app_id
        self.secret = secret if secret is not None else ''
        self.read_apollo = read_apollo

        # 配置是否从apollo读取
        if read_apollo:
            from apollo.apollo_client import ApolloClient
            self.client = ApolloClient(
                self.url,
                self.app_id,
                cluster=self.cluster,
                secret=self.secret
            )
        else:
            self.client = None
        # logger.info("apollo init success...")

    @classmethod
    def get_instance_from_file(cls, cf):
        """
        通过配置文件实例化apollo连接
        :param cf: apollo配置文件
        :return:
        """
        with open(cf, "r", encoding="utf-8") as f:
            cf = yaml.load(f, Loader=yaml.FullLoader)
        acf = cf["config"]["config_center"]
        return cls(
            str(acf["app_id"]),
            url=acf["url"],
            secret=acf["accesskey"].get("secret", ''),
            cluster=acf["cluster"],
            read_apollo=cf["config"]["server"]["is_config_center"]
        )

    def get_value(self, key, namespace='application'):
        """
        根据key及namespace去apollo查询相关配置,
        如果apollo服务挂了的话查本地缓存的apollo配置
        :param key:
        :param namespace:
        :return:
        """
        dt = self.get_namespace(namespace)
        key_list = key.split(".")

        return get_dict_value_by_key_list(dt, key_list)

    def get_namespace(self, namespace='application'):
        """
        :param namespace:
        :return:
        """
        if self.read_apollo:
            ns = self.client.get_namespace(namespace)
        else:
            p = Path(__file__).parent.parent.absolute().joinpath(f"config/{namespace}")
            ns = load_file(p.__str__())

        return ns


apollo_helper = ApolloHelper.get_instance_from_file(
    find_relative_path("config/engine-main.yml")
)

if __name__ == '__main__':
    val = apollo_helper.get_namespace("logger.yml")
    print(val)
