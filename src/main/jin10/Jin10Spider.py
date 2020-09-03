
# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import signals
import win32con,win32gui,time,win32api
import win32clipboard as w
import re
from  datetime import  datetime
hwnd = 394916   #微信窗口句柄，使用句柄工具获取

class Jin10Spider(scrapy.Spider):
    name = 'jinshirili'
    allowed_domains = ['jinshi.com']
    start_urls = ['https://rili.jin10.com/']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Jin10Spider, cls).from_crawler(crawler, *args, **kwargs)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        spider.chrome = webdriver.Chrome(chrome_options=options)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.chrome.quit()
        print('一次爬取结束-----等待下次循环爬取')

    def parse(self, response):

        #获取风险事件列表
        contents = response.xpath('//div[@class="jin-rili_content J_rili_content"]//tr')

        # print(len(contents))
        for i,content in enumerate(contents):
            searchObj = re.search(r'<i class="jin-star_active.*style="width:(.*)%;">', content.extract(),re.I)
            lljd =  content.extract().__contains__("利率决")

            if searchObj or lljd:
                if int(searchObj.group(1)) >= 80 or lljd: #风险等级达到4星或者是利率决定
                    # print("searchObj.group(1) : ", searchObj.group(1))
                    #<p class="jin-table_alignLeft">美国至3月20日美联储利率决定(上限)</p>
                    searchObj = re.search(r'<p.*>[\s\r\n]+([\u4e00-\u9fa50-9a-zA-Z]+)', content.extract(), re.I)
                    event = ""
                    timeS = ""
                    if searchObj :
                        event =  searchObj.group(1)
                        # print("event : ", event)
                    #<td rowspan="2" class="jin-rili_content-time">02:00</td>
                    searchObj = re.search(r'time.*>([0-9:]+)<', content.extract(), re.I)
                    if searchObj:
                        timeS = searchObj.group(1)
                        # print("time : ", time)
                    msg =  event+"  "+timeS
                    # self.sendMsgToWX(msg)

                    #8 12 19点推送到微信
                    if datetime.now().hour == 8 or datetime.now().hour == 12 or datetime.now().hour == 19 :
                        self.sendMsgToWX(msg)

                    print(msg)

    def sendMsgToWX(self, msg):
        # 将微信放在前台
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(2)
        # 将鼠标移到(750, 700)
        win32api.SetCursorPos((750, 700))
        # 单击左键获取焦点
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 750, 700, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 750, 700, 0, 0)
        time.sleep(1)
        # 将内容写入到粘贴板
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, msg.encode(encoding='gbk'))
        w.CloseClipboard()
        time.sleep(1)
        # 单击鼠标右键弹出上下文菜单
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 750, 700, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 750, 700, 0, 0)
        time.sleep(1)
        # 单击鼠标左键点击粘贴
        win32api.SetCursorPos((770, 720))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 770, 720, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 770, 720, 0, 0)
        time.sleep(1)
        # 按回车键发送
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

