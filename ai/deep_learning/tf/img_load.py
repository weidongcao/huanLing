from PIL import Image
import os
from pathlib import Path
import tensorflow as tf

# tfrecords
writer_train = tf.python_io.TFRecordWriter('train.tfrecords')
writer_test = tf.python_io.TFRecordWriter('test.tfrecords')

# 遍历目录(NIST\by_class)
base_path = r''
for filename in os.listdir(base_path):
    # 根据文件夹的名字,我们做转换为十进制,然后读取对应的ascii码
    label = int('0x' + filename, 16) - 65
    for file in os.listdir((base_path + '/' + filename)):
        print(os.path.isfile(file))
        if not os.path.isfile(file) and 'mit' not in file:
            for f in os.listdir(base_path + '/' + filename + '/' + file):
                img = Image.open(base_path + '/' + filename + '/' + file + '/' + f)

                # 重新resize它的大小
                img = img.resize((32, 32))
                img_raw = img.tobytes()

                # 数据写到test.tfrecords
                example = tf.train.Example(feature=tf.train.Features(
                    feature={'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
                             'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))}))

                if 'train' in file:
                    # 序列为字符串
                    writer_test.write(example.SerializeToString())
                else:
                    # 否则写到train.tfrecords
                    # 序列为字符串
                    writer_train.write(example.SerializeToString())
