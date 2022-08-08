# 利用TensorFlow求解根号2
import tensorflow as tf


def sqrt_tf(a):
    x0 = tf.get_variable('x0', initializer=1.0)
    y = (x0 ** 2 - a) ** 2
    # 定义一个优化器
    opt = tf.train.GradientDescentOptimizer(learning_rate=0.001)

    # 对y进行优化
    train_op = opt.minimize(y)

    with tf.Session() as sess:
        # 对所有变量进行初始化
        sess.run(tf.global_variables_initializer())
        # 训练次数
        epoches = 2000
        for _ in range(epoches):
            sess.run(train_op)
        return sess.run(x0)


if __name__ == '__main__':
    a = 2.0
    r = sqrt_tf(a)
    print("sqrt(%s) = %s, %s" % (a, r, r ** 2))

