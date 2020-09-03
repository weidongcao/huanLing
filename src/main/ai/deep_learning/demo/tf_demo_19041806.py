# 测试TensorFlow的分布式集群调用
# 2019年4月18日
import tensorflow as tf

if __name__ == '__main__':
    with tf.device('/gpu:0'):
        a = tf.constant([1, 2, 3], name='a')
        b = tf.constant(2, name='b')
        c = a * b

    # 新建Session
    # log_device_placement=True表示打印TensorFlow设备信息
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    print(sess.run(c))

    # mat1 = tf.constant([3, 3], dtype=tf.float32, shape=[1,2])
    # mat2 = tf.constant([[3.], [3.]])
    # product = tf.matmul(mat1, mat2)
    # sess.run(product)
