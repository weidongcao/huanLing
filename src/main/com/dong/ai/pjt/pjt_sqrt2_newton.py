# 利用牛顿法求解根号2


def sqrt_newton(a):
    y = lambda x : x ** 2
    y_x = lambda x : 2 * x
    dy = lambda a, x: a - y(x)
    dx = lambda a, x: dy(a, x) / y_x(x)

    x0 = 1.0
    for _ in range(20):
        x0 += dx(a, x0)
    return x0


if __name__ == '__main__':
    a = 2.0
    print("sqrt(%s) = %s" % (a, sqrt_newton(a)))

