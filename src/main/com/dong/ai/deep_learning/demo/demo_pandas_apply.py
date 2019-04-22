"""
pandas包的apply函数的使用
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.apply.html
"""
import pandas as pd


def sum_num(record):
    r = zip(record)
    result = 0
    for value in r:
        result = result + value[0]
    return  result


def square_column_num(names, record):
    result=[]
    r = zip(names, record)
    for name, value in r:
        if name == 1:
            value = value * value
        result.append(value)
    return result


def square_row_num(names, record):
    result=[]
    r = zip(names, record)
    for name, value in r:
        if name == 'bb':
            value = value * 2
        result.append(value)
    return result


if __name__ == '__main__':
    names = ['home', 'bb', 'cc']
    indexs = [0, 1, 2]
    datas = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    df = pd.DataFrame(datas, columns=names)
    print('-------------------------------------------')
    print('original --> ')
    print(type(df))
    print(df)
    print('-------------------------------------------')
    data1 = df.apply(lambda x: x * x)
    print('data1 -->')
    print(type(data1))
    print(data1)

    print('-------------------------------------------')
    data2 = df.apply(lambda record: square_column_num(indexs, record))
    print('data2 -->')
    print(type(data2))
    print(data2)

    print('-------------------------------------------')
    data3 = df.apply(lambda record: square_row_num(names, record), axis=1)
    print("data3 -->")
    print(type(data3))
    print(data3)

    print('-------------------------------------------')
    data4 = df.apply(lambda record: square_row_num(names, record), axis=1, result_type='broadcast')
    print('data4 -->')
    print(type(data4))
    print(data4)

    print('-------------------------------------------')
    data5 = df.apply(lambda record: sum_num(record))
    print('data5 -->')
    print(type(data5))
    print(data5)

    print('-------------------------------------------')
    data6 = df.apply(lambda record: sum_num(record), axis=0, result_type='broadcast')
    print('data6 -->')
    print(type(data6))
    print(data6)

    print('-------------------------------------------')
    data7 = df.apply(lambda record: sum_num(record), axis=1, result_type='broadcast')
    print('data7 -->')
    print(type(data7))
    print(data7)

    print('-------------------------------------------')
    data8 = df.apply(lambda record: sum_num(record), raw=True)
    print('data8 -->')
    print(type(data8))
    print(data8)

    print('-------------------------------------------')
    data9 = df.apply(lambda record: sum_num(record), result_type='reduce')
    print('data9 -->')
    print(type(data9))
    print(data9)