import tensorflow as tf
import numpy as np


# 使用队列读取文件
def read_and_decode(filename):
    # 读取文件按照字符串的方式
    filename_queue = tf.train.string_input([filename])
    # 使用TFRecordReader()解析
    reader = tf.TFRecordReader()
    _, serialized = reader.read(filename_queue)  # 文件名和文件
    features = tf.parse_single_example(serialized, features={'label': tf.FixedLenFeature([], tf.int64),
                                                             'img_raw': tf.FixedLenFeature([], tf.string)})
    img = tf.decode_raw(features['label'], tf.int32)

    img  = tf.cast(img ,tf.float32) / 255
    label = tf.cast(features['label'], tf.int32)
    label_zeros = np.zeros([label.shape[0], 26])
    label_zeros[label] = 1

    # 将label转换为one_hot类型
    return img, label_zeros

img, label = read_and_decode('test.tfrecords')

# shuffle_batch 可以随机打乱数据
# batch_size批量数据
# capacity 队列的长度
# num_threads 从队列中抽取数据的线程数
img_batch, label_batch = tf.train.shuffle_batch([img, label], batch_size=30, capacity=200, num_threads=4)

# 构建网络
X = tf.placeholder(tf.float32, [None, 32,32,1])
Y = tf.placeholder(tf.int, [None, 26])

def net():
    # conv1
    conv1_weight = tf.get_variable('conv1_b', [5,5,1,6])
    conv1_bias = tf.get_variable('conv1_b', [6])
    conv1 = tf.bias_add(tf.nn.conv2d(X, conv1_weight),strides=[1,1,1,1], padding='VALID')#conv1_bias)

    print(conv1)

    conv1_pooling = tf.nn.max_pooling(conv1,filter=[1,2,2,1], strides=[1,2,2,1], padding='VALID')

    print(conv1_pooling)

    # 28, 28, 6

    # conv2
    conv2_weight_1 = tf.get_variable('conv2_w', [5,5,2,1])
    conv2_bias_1 = tf.get_variable('conv2_b', [1])
    conv2_tensor = tf.constant(np.zeros[30,28,28,16])

    for i in range(0, 6, 1):
        # 0-2 1-3 2-4 3-5
        # 4-5+1, 5+1+2
        conv2 = tf.bias_add(tf.nn.conv2d(conv1_pooling[i:i+3], conv2_weight_1), strides=[1,1,1,1], padding='VALID')# conv2_bias_1)
        conv2_tensor[:, :, :, i] = conv2
    conv2_tensor[:,:,:,4] = tf.bias_add(tf.nn.conv2d(tf.concat([conv1_pooling[4:], conv1_pooling[0]]), conv2_weight_1), strides=[1,1,1,1], padding='VALID')# conv2_bias_1)

    conv2_tensor[:,:,:,5] = tf.bias_add(tf.nn.conv2d(tf.concat([conv1_pooling[5], conv1_pooling[0:2]]), conv2_weight_1), strides=[1,1,1,1], padding='VALID')# conv2_bias_1)

    # .....
    conv2_pooling= tf.nn.max_pooling(conv2_tensor, filter=[1,2,2,1], strides=[1,2,2,1], padding='VALID')
    print(conv2_pooling)




