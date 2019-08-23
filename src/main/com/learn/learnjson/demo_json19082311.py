# -*- coding: UTF-8 -*-
import json

from com.utils.common_util import weidong_print


def test_dump():
    s = json.dumps(['yeeku', {'favorite': ('coding', None, "Name", 25)}])
    weidong_print(s)

    s2 = json.dumps("\"foo\bar")
    weidong_print(s2)

    s3 = json.dumps('\\')
    weidong_print(s3)

    s4 = json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    weidong_print(s4)

    s5 = json.dumps([1, 2, 3, {'x': 5, 'y': 7}], separators=(',', ':'))
    weidong_print(s5)

    s6 = json.dumps({'Python': 5, 'Kotlin': 7}, sort_keys=True, indent=4)
    weidong_print(s6)

    s7 = json.JSONEncoder().encode({"names": (u'孙悟空', u'齐天大圣')})
    weidong_print(s7)

    with open('i.json', 'w') as f:
        json.dump(['Kotlin', {'Python': 'excellent'}], f)


def test_load():
    l1 = json.loads('["yeeku", {"favorite": ["coding", null, "game", 25]}]')
    weidong_print(l1)

    l2 = json.loads('"\\"foo\\"bar"')
    weidong_print(l2)

    def as_complex(dct):
        if '__complex__' in dct:
            return complex(dct['real'], dct['imag'])
        return dct

    # 使用自定义的恢复函数
    # 自定义恢复函数将real数据转成复数的实部，将imag转成复数的虚部
    l3 = json.loads('{"__complex__": true, "real": 1, "imag": 2}', object_hook=as_complex)
    weidong_print(l3)

    f = open('a.json')
    l4 = json.load(f)
    weidong_print(l4)


def test_write():
    name_emb = {'a': '1111', 'b': '2222', 'c': '3333', 'd': '4444'}

    emb_filename = ('emb_json.json')

    # jsObj = json.dumps(name_emb)

    with open(emb_filename, "w") as f:
        f.write(name_emb)


if __name__ == '__main__':
    test_dump()
    test_load()
    test_write()
