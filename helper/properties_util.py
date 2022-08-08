# -*- coding: UTF-8 -*-

import re
import os
import tempfile
from pathlib import Path


class Properties:
    def __init__(self, file_name):
        self.file_name = Path(file_name)
        self.properties = {}
        if self.file_name.exists():
            try:
                f = open(self.file_name, 'r')
                for line in f:
                    line = line.strip()
                    if line.find('=') > 0 and not line.startswith('#'):
                        k, v = line.split('=')
                        k = k.strip()
                        if "," in v:
                            v = [int(e.strip()) if e.strip().isdigit() else e.strip() for e in v.split(",")]
                        elif v.strip().isdigit():
                            v = int(v.strip())
                        else:
                            v = v.strip()
                        if k in self.properties:
                            if type(self.properties[k]) == list:
                                l = self.properties[k]
                                if type(v) == list:
                                    l.extend(v)
                                else:
                                    l.append(v)
                                self.properties[k] = l
                            else:
                                self.properties[k] = [self.properties[k], v]
                        else:
                            self.properties[k.strip()] = v
            except Exception as e:
                raise e
            f.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=None):
        v = default_value
        if key in self.properties:
            v = self.properties.get(key)
        return v

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + str(value), True)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    tmp_file = tempfile.TemporaryFile()

    if not file_name.exists():
        file_name.touch()

    r_open = open(file_name, 'r')
    pattern = re.compile(r'' + from_regex)
    found = None
    for line in r_open:
        if pattern.search(line) and not line.strip().startswith('#'):
            found = True
            line = re.sub(from_regex, to_str, line)
        tmp_file.write(line.encode())
    if not found and append_on_not_exists:
        tmp_file.write(('\n' + to_str).encode())
    r_open.close()
    tmp_file.seek(0)

    content = tmp_file.read()

    if os.path.exists(file_name):
        os.remove(file_name)

    w_open = open(file_name, 'wb')
    w_open.write(content)
    w_open.close()

    tmp_file.close()


if __name__ == "__main__":
    file_path = 'test.properties'
    props = Properties(file_path)  # 读取文件
    # props.put('jdbc.url', 'value_a')  # 修改/添加key=value
    print(props.get('dag1.task1.dependence'))  # 根据key读取value
    print(type(props.get('dag1.task1.dependence')))  # 根据key读取value
    print(props.get('dag1.task1.timeout'))  # 根据key读取value
    print(type(props.get('dag1.task1.timeout')))  # 根据key读取value
    print("props.has_key('key_a')=" + str(props.has_key('key_a')))  # 判断是否包含该key
    print(props.put("wedo", 123456))
