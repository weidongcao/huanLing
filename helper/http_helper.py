# -*- coding:utf-8 -*-
import base64
import json
from pprint import pprint

import requests

from entity.task_instance import TaskInfo
from helper import util

airflow_conf = util.load_file(util.find_relative_path("config/airflow.yml")).get("airflow")
host = airflow_conf.get("host")
port = airflow_conf.get("port")
username = airflow_conf.get("username")
password = airflow_conf.get("password")
authorization = airflow_conf.get("auth")


def request(method_type="GET", url=None, data=None, cls=dict):
    """:
    entity must have property status_code to store http response code(200, 404, 500)
    """
    a = f"{username}:{password}"
    auth_info = str(base64.b64encode(a.encode('utf-8')), "utf-8")
    headers = {
        "Authorization": f"{authorization.capitalize()} {auth_info}",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
        "origin": "https://www.baidu.com",
        "Referer": "http://192.168.177.147:55370/home"
    }

    response = requests.request(method=method_type.upper(), url=url, headers=headers, data=data)

    e = json.loads(response.text)
    e["status_code"] = response.status_code

    if 200 != response.status_code and "status" in e:
        e["status_code"] = response.status_code
        del e["status"]

    return cls(**e)



if __name__ == '__main__':

    # api = "http://192.168.177.147:55370/api/v1/dags/wedo-dag/dagRuns/wedo-task-1min/taskInstances/scheduled__2021-07-08T08:47:00+00:00"
    api = "http://192.168.177.147:55370/api/v1/dags/yamu-dag-2min/dagRuns/scheduled__2021-07-12T06:36:01+00:00/taskInstances/yamu-task-2min"

    a = request("GET", api, cls=TaskInfo)
    # a = request("GET", api, cls=TaskInfo)
    print(a.message())

    # t = TaskInstance(None, None)
    # t.__dict__.update(**a)
    # pprint(t.__dict__)