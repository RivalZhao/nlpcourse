import numpy as np
arr = np.array([[1, 2], [3, 4]])

test_num = 2345678
arr_ele_num = int(test_num)
dimension = int(np.ceil(np.sqrt(arr_ele_num)))
if dimension % 2 == 0:
    dimension = dimension + 1
arr = np.ones((dimension, dimension))
print(arr)

initial_i = np.floor(dimension/2)
initial_j = np.floor(dimension/2)
i = int(initial_i)
j = int(initial_j)
direction_add_num = 0 #在当前方向添加次数
direction_add_amount = 0 #在当前方向添加总数
conversion_direction_num = 0 #转换方向次数
direction = 1
symbol = 1 #1加  2减
symbol_num = 2
for ele in range(np.square(dimension)):
    #print("i:"+str(i)+" J:"+str(j))
    arr[i][j] = ele + 1
    if direction_add_num == direction_add_amount: #当前方向次数等于总数 转换方向
        direction_add_num = 0
        if conversion_direction_num % 2 == 0:
            #转换两次方向 单方向总数+1
            direction_add_amount = direction_add_amount + 1
        conversion_direction_num = conversion_direction_num + 1
        #转方向
        if direction == 1:
            direction = 2
        else:
            direction = 1
        #每两个方向，变更一次符号
        symbol_num = symbol_num - 1
        if symbol_num == 0:
            symbol_num = 2
            if symbol == 1:
                symbol = 2
            else:
                symbol = 1
    if direction == 1:
        if symbol == 1:
            i = i + 1
        else:
            i = i - 1
    else:
        if symbol == 1:
            j = j + 1
        else:
            j = j - 1

    direction_add_num = direction_add_num + 1

print(arr)


where = np.argwhere(arr == test_num)
test_num_i = where[0][0]
test_num_j = where[0][1]

'''
where = np.argwhere(arr == (test_num+1))
test_near_num_i = where[0][0]
test_near_num_j = where[0][1]
'''
print(where)

confirm_i = 0
confirm_j = 0
confirm = 1 #1确定i  2确定j
'''
if ((test_num_i - test_near_num_i) == 1) or ((test_num_i - test_near_num_i) == -1):
    confirm_i = np.floor(dimension/2) - test_num_i
if ((test_num_j - test_near_num_j) == 1) or ((test_num_j - test_near_num_j) == -1):
    confirm_j = np.floor(dimension/2) - test_num_j
'''
#print(int(np.floor(dimension/2)))
#print(int(test_num_j))
print('----')
confirm_i = int(np.floor(dimension/2)) - int(test_num_i)
confirm_j = int(np.floor(dimension/2)) - int(test_num_j)
print(np.fabs(confirm_i) + np.fabs(confirm_j))

