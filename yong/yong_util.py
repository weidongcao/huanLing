"""
工具类
"""


def dict_to_wubi_code(dt, fps, encoding):
    clist = []
    for key, value in dt.items():
        clist.append(key + ' ' + ' '.join(value))
    clist.sort()
    with open(fps, 'w', encoding=encoding) as file:
        file.write('\n'.join(clist))

def list_to_wubi_code(lt, fps, encoding):

    with open(fps, 'w', encoding=encoding) as file:
        file.write('\n'.join(lt))