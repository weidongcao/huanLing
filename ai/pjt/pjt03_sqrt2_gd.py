# 利用梯度下降法求解根号2

def sqrt_gd(num):
    y = lambda num, x: (x ** 2) ** 2
    y_x = lambda num, x: 2 *  (x ** 2 -num) * (2 * x)
    dx = lambda alpha,a,x: -alpha * y_x(a, x)

    x0 = 1.0
    alpha = 0.001
    for _ in range(2000):
        x0 += dx(alpha, num, x0)
    return x0


if __name__ == '__main__':
    a = 2.0
    r = sqrt_gd(a)
    print("sqrt(%s) = %s, %s" % (a, r, r ** 2))

