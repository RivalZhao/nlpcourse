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

def radom_get_kb():
    X_rm = X[:, 5]
    trying_times = 20000

    min_loss = float('inf')
    best_k, best_b = None, None

    for i in range(trying_times):
        k = random.random() * 200 - 100
        b = random.random() * 200 - 100
        price_by_random_k_and_b = [price(r, k, b) for r in X_rm]

        current_loss = loss_squared(Y, price_by_random_k_and_b)

        if current_loss < min_loss:
            min_loss = current_loss
            best_k, best_b = k, b
            print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b, min_loss))

    price_by_random_k_and_b = [price(r, best_k, best_b) for r in X_rm]
    draw_rm_and_price(X, Y)
    plt.scatter(X_rm, price_by_random_k_and_b)
    plt.show()


def direction_get_kb():
    X_rm = X[:, 5]
    trying_times = 20000
    min_loss = float('inf')
    best_k = random.random() * 200 - 100
    best_b = random.random() * 200 - 100
    direction = [
        (+1, -1),  # first element: k's change direction, second element: b's change direction
        (+1, +1),
        (-1, -1),
        (-1, +1),
    ]
    next_direction = random.choice(direction)
    scalar = 1
    update_time = 0
    for i in range(trying_times):
        k_direction, b_direction = next_direction
        if i > 10000:
            scalar = 0.1
        current_k, current_b = best_k + k_direction * scalar, best_b + b_direction * scalar
        price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
        current_loss = loss_squared(Y, price_by_k_and_b)
        if current_loss < min_loss:  # performance became better
            min_loss = current_loss
            best_k, best_b = current_k, current_b
            next_direction = next_direction
            update_time += 1
            if update_time % 2 == 0:
                print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b,
                                                                                                      min_loss))
        else:
            next_direction = random.choice(direction)

    price_by_random_k_and_b = [price(r, best_k, best_b) for r in X_rm]
    draw_rm_and_price(X, Y)
    plt.scatter(X_rm, price_by_random_k_and_b)
    plt.show()


def loss_abs(y, y_hat):
    return sum(abs(y_i - y_hat_i) for y_i, y_hat_i in zip(y, y_hat)) / len(y)


def direction_abs_get_kb():
    X_rm = X[:, 5]
    trying_times = 20000
    min_loss = float('inf')
    best_k = random.random() * 200 - 100
    best_b = random.random() * 200 - 100
    direction = [
        (+1, -1),  # first element: k's change direction, second element: b's change direction
        (+1, +1),
        (-1, -1),
        (-1, +1),
    ]
    next_direction = random.choice(direction)
    scalar = 1
    update_time = 0
    for i in range(trying_times):
        k_direction, b_direction = next_direction
        if i >2000:
            scalar = 0.1
        current_k, current_b = best_k + k_direction * scalar, best_b + b_direction * scalar
        price_by_k_and_b = [price(r, current_k, current_b) for r in X_rm]
        current_loss = loss_abs(Y, price_by_k_and_b)
        if current_loss < min_loss:  # performance became better
            min_loss = current_loss
            best_k, best_b = current_k, current_b
            next_direction = next_direction
            update_time += 1
            if update_time % 2 == 0:
                print('When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, best_k, best_b,
                                                                                                      min_loss))
        else:
            next_direction = random.choice(direction)

    price_by_random_k_and_b = [price(r, best_k, best_b) for r in X_rm]
    draw_rm_and_price(X, Y)
    plt.scatter(X_rm, price_by_random_k_and_b)
    plt.show()


# radom_get_kb()

# direction_get_kb()

direction_abs_get_kb()