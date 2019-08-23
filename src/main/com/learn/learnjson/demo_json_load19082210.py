# -*- coding: UTF-8 -*-
# @Anthor : weidong
# @Email : weidong@gmail.com
# @Created: 2019年8月22日

import json
if __name__ == '__main__':
    file = 'info.json'
    with open(file, 'r', encoding='utf8') as f:
        # 以json.load()方法加载json文件
        # python的json模块主要有4个方法：
        #   1. json.dumps: 把Python对象解析为json对象，其实就是字典
        #   2. json.dump :
        j = json.load(f)
        print(j)

        # print(json.dumps(j, indent=4, sort_keys=False, ensure_ascii=False))
