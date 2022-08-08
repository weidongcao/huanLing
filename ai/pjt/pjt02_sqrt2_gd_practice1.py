# 利用梯度下降法求解根号2

def solve_gd(num):
    y = lambda x1, x2: (x1 - 3) ** 2 + (x2 - 4) ** 2
    y_x1 = lambda x1, x2: 2 * (x1 - 3)
    y_x2 = lambda x1, x2: 2 * (x2 - 4)
    dx1 = lambda alpha, x1, x2: -alpha * y_x1(x1, x2)
    dx2 = lambda alpha, x1, x2: -alpha * y_x2(x1, x2)

    x1, x2 = 1.0, 1.0
    alpha = 0.001
    for _ in range(2000):
        x1 = dx1(alpha, x1, x2)
        x2 = dx2(alpha, x1, x2)

    return x1, x2


if __name__ == '__main__':
    a = 2.0
    r = solve_gd(a)
    print("sqrt(%s) = %s, %s" % (a, r, r ** 2))

