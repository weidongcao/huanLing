"""
参考博客：
https://germey.gitbooks.io/python3webspider/content/1.6.1-Flask%E7%9A%84%E5%AE%89%E8%A3%85.html?q=
用于测试Python3的Flask模块是否安装成功

Flask是一个轻量级的Web服务程序，简单、易用、灵活
Python安装Flask:
pip3 install flask
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
