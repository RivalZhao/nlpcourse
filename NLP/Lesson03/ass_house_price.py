from sklearn.datasets import load_boston
import matplotlib.pyplot as plt
import random

data = load_boston()
X, Y = data['data'], data['target']


def draw_rm_and_price(X, Y):
    plt.scatter(X[:, 5], Y)  # 房屋数量x 与 价格y
    # plt.show()


def price(rm, k, b):
    return k * rm + b


def loss_squared(y, y_hat):
    return sum((y_i - y_hat_i)**2 for y_i, y_hat_i in zip(y, y_hat)) / len(y)

#draw_rm_and_price(X, Y)


def partial_k(x, y, y_hat):
    n = len(y)
    gradient = 0
    for x_i, y_i, y_hat_i in zip(list(x), list(y), list(y_hat)):
        gradient += (y_i - y_hat_i) * x_i
    return -2 / n * gradient


def partial_b(x, y, y_hat):
    n = len(y)
    gradient = 0
    for y_i, y_hat_i in zip(list(y), list(y_hat)):
        gradient += (y_i - y_hat_i)
    return -2 / n * gradient


def gradient_get_kb():
    X_rm = X[:, 5]
    trying_times = 20000
    min_loss = float('inf')
    current_k = random.random() * 200 - 100
    current_b = random.random() * 200 - 100
    learning_rate = 1e-02

    for i in range(trying_times):
        price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
        current_loss = loss_squared(Y, price_by_k_and_b)
        if i % 100 == 0:
            print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b,
                                                                                                      current_loss))
        k_gradient = partial_k(X_rm, Y, price_by_k_and_b)
        b_gradient = partial_b(X_rm, Y, price_by_k_and_b)
        current_k = current_k + (-1 * k_gradient) * learning_rate
        current_b = current_b + (-1 * b_gradient) * learning_rate

    price_by_final_k_and_b = [price(r, current_k, current_b) for r in X_rm]
    draw_rm_and_price(X, Y)
    plt.scatter(X_rm, price_by_final_k_and_b)
    plt.show()


gradient_get_kb()

# gradient_get_kb()