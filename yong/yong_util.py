"""
工具类
"""


def dict_to_wubi_code(dt, fps, encoding):
    """
    Python字典(保存小小输入法的码表)写入五笔文件,并指定编码格式
    :param dt: 保存小小输入法码表的字典
    :param fps: 小小输入法个人词库路径
    :param encoding: 编码格式,一般为GB18030
    """
    clist = []
    for key, value in dt.items():
        clist.append(key + ' ' + ' '.join(value))
    clist.sort()
    with open(fps, 'w', encoding=encoding) as file:
        file.write('\n'.join(clist))

def list_to_wubi_code(lt, fps, encoding):

    with open(fps, 'w', encoding=encoding) as file:
        file.write('\n'.join(lt))
