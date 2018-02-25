"""
用于测试Urllib库里parse模块
这个模块定义了处理URL的标准接口
例如实现URL各部分的抽取，合并以及罗拉转换。
"""
import urllib
from urllib.parse import urlparse
from urllib.parse import urlunparse

urlstring = "http://www.baidu.com/index.html;user?id=5#comment"
result = urlparse(urlstring)
print(type(result), result)

urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)

result = urlparse("www.baidu.com/index.html;user?id=5#comment", scheme='https')
print(result)

data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(urlunparse(data))
