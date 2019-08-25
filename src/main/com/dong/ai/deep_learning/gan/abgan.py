# ebgan
import tensorflow as tf

import os
import numpy as np
import random

from PIL import Image
import scipy.misc as misc

data_dir = 'img_align_celeba'

# 获取数据矩阵

train_image = []
for file in os.listdir(data_dir):
    if file.endswith('.jpg'):
        # 路径
        train_image.append(os.path.join(data_dir, file))

# 数据打乱
random.shuffle(train_image)

# 设置一些参数,为batch批数据生成做准备
batch_size = 32
# batch_size 一个数据集会最多少次
num_batch = len(train_image) // batch_size

# 设置resize 的参数
image_size = 64
image_channel = 3

def get_next_batch(index):
    image_batch = []
    images = train_image[index * batch_size : (index + 1) * batch_size]

    for img in images:
        arr = Image.open(img)
        arr = arr.resize((image_size, image_size)) # 64 * 64
        arr = np.array(arr) # 图像对象转换为图像数组
        arr = arr.astype(np.float32)
        image_batch.append(arr)

    return image_batch

# 构建生成器
z_dim = 100
noise = tf.placeholder(tf.float32, [None, z_dim])

X = tf.placeholder(tf.float32, [batch_size, image_size, image_size, image_channel])

# 因为模型中有BN操作(BN会使用滑动平均),在测试过程中,不需要执行滑动平均操作,
# 所以需要加入一个是否训练的表示
# 测试过程中,直接返回滑动平均后的对应均值和方法,但是不更新到变量中.
train_tf = tf.placeholder(tf.bool)

# 构建BN全局归一化
def batch_norm(x, beta, gamma, tf_train, decay=0.9):
    # 首先计算平均值和方差,使用滑动平均模型来控制生成平均值和方差
    # moments(数据,求解的维度)
    # 计算均值和方差
    batch_mean, batch_var = tf.nn.moments(x, [0, 1, 2])

    # 嵌入滑动平均模型,控制均值和方差的数值
    ema = tf.train.ExponentialMovingAverage(decay=decay)

    def mean_var_with_update():
        ema_apply_op = ema.apply([batch_mean, batch_var])
        # 滑动平均之后,影子变量更新到原始变量中
        with tf.control_dependencies([ema_apply_op]):
            return tf.identity(batch_mean), tf.identity(batch_var)

    # cond(条件, f1, f2)
    mean, var = tf.cond(tf_train, mean_var_with_update(), lambda : (ema.average(batch_mean), ema.average(batch_var)))


    # 进行标准化,BN操作
    normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, eps=1e-5)
    return normed

    # 构建生成器
    # input [ batch_size, z_dim] => w * x + b => reshape [batch_size, IMAGE_SIZE // 16, IMAGE_SIZE // 16, 3
    generator_variable_dict = {
        'W_1': tf.Variable(tf.random_normal([z_dim, 4 * image_size * image_size], stddev=0.02)),
        'B_1': tf.Variable(tf.random_normal([4 * image_size * image_size], stddev=0.1)),
        'beat_1': tf.Variable(tf.constant(0.0, [4 * image_size * image_size])),
        'gamma_1': tf.Variable(tf.random_normal([1024], mean=1.0, stddev=0.01)),

        'W_2': tf.Variable(tf.random_normal([5,5, 512, 1024], stddev=0.02)),
        'B_2': tf.Variable(tf.random_normal(0.0, [128])),
        'beat_2': tf.Variable(tf.constant(0.0, [128])),
        'gamma_2': tf.Variable(tf.random_normal([128], mean=1.0, stddev=0.01)),

        'W_3': tf.Variable(tf.random_normal([5, 5, 128, 512], stddev=0.02)),
        'B_3': tf.Variable(tf.random_normal([512], stddev=0.1)),
        'beat_3': tf.Variable(tf.constant(0.0, [128])),
        'gamma_3': tf.Variable(tf.random_normal([128], mean=1.0, stddev=0.01)),

        'W_4': tf.Variable(tf.random_normal([5, 5, 64, 128], stddev=0.02)),
        'B_4': tf.Variable(tf.random_normal([64], stddev=0.1)),
        'beat_4': tf.Variable(tf.constant(0.0, [64])),
        'gamma_4': tf.Variable(tf.random_normal([64], mean=1.0, stddev=0.01)),

        'W_5': tf.Variable(tf.random_normal([5,5,image_channel, 64], stddev=0.02)),
        'B_5': tf.Variable(tf.constant(0.0, [image_channel]))
    }

# def generator(noise):
#     out_1 = tf.nn.xw_plus_b(noise, generator_variable_dict['W_1'], generator_variable_dict['B_1'])
#     out_1 = tf.nn.xw_plus_b(out_1, [-1, image_size // 16, image_size // 16, 1024])
#     out_1 = batch_norm(out_1, generator_variable_dict['beta_1'], generator_variable_dict['gamma_1'], train_tf)
#     out_1 = tf.nn.relu(out_1)
#
#     # conv2d_transpose(input, filter, out_shape, strides, padding
#     out_2 = tf.nn.conv2d_transpose(out_1, generator_variable_dict['W_2'], output_shape=[batch_size, image_size // 8, image_size // 8, 512], strides=[1,2,2,1], padding='SAME')