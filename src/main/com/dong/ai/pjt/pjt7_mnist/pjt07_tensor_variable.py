import tensorflow as tf

a = 3
a = a * 5
print(a)

b = tf.constant(3)
b = b * 5
print(b)

c = tf.placeholder(tf.int32)
c2 = c
c = c * 5
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(sess.run(b))
    print(sess.run(c, {c2: 4}))
