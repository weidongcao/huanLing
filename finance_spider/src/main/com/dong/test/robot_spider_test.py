"""
测试爬虫协议
"""
from urllib.robotparser import RobotFileParser
from urllib.request import urlopen
rp = RobotFileParser()

rp.set_url('http://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'http://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', "http://www.jianshu.com/search?q=python&page=1&type=collections"))



