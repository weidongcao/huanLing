import urllib.request
"""
Urllib库里还提供了Parse这个模块，它定义了处理URL的标准接口，例如
实现URL各部分的抽取，合并以及链接转换。它支持如下的URL处理：file、
ftp、gopher、hdl、http、https、imap、mailto、mms等等。
"""
response = urllib.request.urlopen('https://www.jin10.com/')
print(type(response))
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))

print(response.read().decode("utf-8"))
