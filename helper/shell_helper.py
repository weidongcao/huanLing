# -*- coding:utf-8 -*-
import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def exec_shell(cmd, cur_dir=os.path.dirname(__file__)):
    result_cmd = subprocess.Popen(cmd, cwd=cur_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=True)
    logger.info(f"execute linux command:--> {cmd}")
    # 等等命令行运行完
    result_cmd.wait()

    # 获取命令行输出
    stdout = result_cmd.stdout.read()

    # 获取命令行异常
    stderr = result_cmd.stderr.read()

    # 获取shell 命令返回值,如果正常执行会返回0, 执行异常返回其他值
    result_code = result_cmd.returncode

    # 获取命令运行进程号
    pid = result_cmd.pid

    info = {
        "stdout": str(stdout, encoding="utf-8").strip(),
        "stderr": str(stderr, encoding="utf-8").strip(),
        "result_code": result_code,
        "pid": pid
    }
    # if result_code != 0:
    #     raise Exception(info)

    return info


if __name__ == "__main__":
    # cwdpath = "/home/caoweidong/python/practice/"
    # cwdpath = "com/don/monitor_table/"
    cwdpath = "D:\\bigdata\\workspace\\PycharmProjects\\python\\com\\don\\monitor_table\\"

    result_dict = exec_shell("python TestPython.py ddd", cwdpath)

    print("stdout = " + str(result_dict["stdout"]))
    print("stderr = " + str(result_dict["stderr"]))
    print("pid = " + str(result_dict["pid"]))
    print("returncode = " + str(result_dict["returncode"]))
