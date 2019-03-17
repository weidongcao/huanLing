# 利用梯度下降法求f(x) = (x_{1} - 3)^{2} + (x_{2} - 4)^{2}的最小值位置
import tensorflow as tf
def sqrt_gd():
    x1 = tf.get_variable('x1', initializer=1.)
    x2 = tf.get_variable('x2', initializer=1.)

    y = (x1 - 3) ** 2 + (x2 - 4) ** 2
    opt = tf.train.AdamOptimizer(learning_rate=0.001)
    train_op = opt.minimize(y)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        epoches = 20000
        for _ in range(epoches):
            sess.run(train_op)
        return sess.run([x1, x2])


if __name__ == '__main__':
    a = 2.0
    x1, x2 = sqrt_gd()
    print("x1 = %s, x2 = %s" % (x1, x2))

