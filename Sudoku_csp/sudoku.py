'''
This file includes some functions for solving the sudoku questions
'''
import copy
import time
import numpy as np
'''
A sudoku can be discribed as:
    suduku = 
[
         0 1 2  3 4 5  6 7 8
    0    x x x |x x x |x x x
    1    x x x |x x x |x x x
    2    x x x |x x x |x x x
         -------------------
    3    x x x |x x x |x x x
    4    x x x |x x x |x x x
    5    x x x |x x x |x x x
         -------------------
    6    x x x |x x x |x x x
    7    x x x |x x x |x x x
    8    x x x |x x x |x x x        
]

Can be divided into 9 blocks:
        b0(0/0)   b1(0/3)   b2(0/6)
        b3(3/0)   b4(3/3)   b5(3/6)
        b6(6/0)   b7(6/3)   b8(6/6)
'''
# 读取数独问题
def read_file(file_name):
    data = np.loadtxt('todo/' + file_name)
    data.astype(int)
    list = data.tolist()
    for i in range(9):
        for j in range(9):
            list[i][j] = int(list[i][j])
    return list
# 输出结果与相关数据
def output(filename, data, type, info):
    path = "solution/" + filename + "_solution.txt"
    file = open(path, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符

        file.write(s)
    t = ""
    t += "solve method:" + type + "\n" + info + "\n"
    t += "-----------------------------------------------------\n"
    file.write(t)
    file.close()
    return

# this function is used for check if the sudoku has been finished
# 检查数独表是否完成
def is_finished(input):
    result = 1
    # check row
    for i in range(9):
        temp = copy.deepcopy(input[i])
        temp.sort()
        if temp != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
        else:
            result *= 1
    # check colume
    for i in range(9):
        temp = []
        for j in range(9):
            temp.append(input[i][j])
        temp.sort()
        if temp != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
        else:
            result *= 1
            continue
    # check block
    for i in range(9):
        temp = []
        for m in range(3):
            for n in range(3):
                temp.append(input[(3 * int(i / 3)) + m][(3 * int(i % 3)) + n])
        temp.sort()
        if temp != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
        else:
            result *= 1
            continue
    return True

# this function is to check the point value
# 回溯方法判断条件
def CSP_check_point(map, row, col, value):
    # check in row
    for i in range(9):
        if (map[row][i] == value) and (i != col):
            return False
    #check in col
    for i in range(9):
        if (map[i][col] == value) and (i != row):
            return False
    #check in block
    temp_row = int(row / 3) * 3
    temp_col = int(col / 3) * 3
    for i in range(temp_row, temp_row + 3):
        for j in range(temp_col, temp_col + 3):
            if (map[i][j] == value) and (i != row) and (j != col):
                return False

    return True

# this function is to find the position which value = 0
# Attention: when the map is full -> return false !!! or return true
# 得到空闲位置
def find_empty_position(input, start_pos):
    for i in range(9):
        for j in range(9):
            if input[i][j] == 0:
                start_pos[0] = i
                start_pos[1] = j
                return True
    return False
# 获取row,col的可选填数字
def get_available_number(input, row, col):
        available = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        exsist = []
        # scan the row
        for i in range(9):
            if input[row][i] != 0 and i != col:
                exsist.append(input[row][i])
        # scan the col
        for i in range(9):
            if input[i][col] != 0 and i != row:
                exsist.append(input[i][col])

        # scan the block
        temp_row = int(row / 3) * 3
        temp_col = int(col / 3) * 3
        for i in range(temp_row, temp_row + 3):
            for j in range(temp_col, temp_col + 3):
                if input[temp_row][temp_col] != 0 and temp_col != col and temp_row != row:
                    exsist.append(input[temp_row][temp_col])

        exsist = list(set(exsist))
        # print list(set(b).difference(set(a)))  # b中有而a中没有的
        result = list(set(available).difference(set(exsist)))
        # result = result.sort()
        return result
# MRV 判断条件
def MRV_check_point(map, row, col, value):
    # check in row

    for i in range(9):
        t = get_available_number(map, i, col)
        if ((len(t) == 1) and t[0] == value and (i != row)) or ((map[row][i] == value)):
            return False
    #check in col
    for i in range(9):
        t = get_available_number(map, row, i)
        if ((len(t) == 1) and t[0] == value and (i != col)) or((map[i][col] == value)):
            return False
    #check in block
    temp_row = int(row / 3) * 3
    temp_col = int(col / 3) * 3
    for i in range(temp_row, temp_row + 3):
        for j in range(temp_col, temp_col + 3):
            t = get_available_number(map, i, j)
            if ((len(t) == 1) and t[0] == value and(i != row) and (j != col)) or ((map[i][j] == value)):
                return False
    return True
# GAC判断条件
def GAC_check_point(map, row, col, value):
    temp = copy.deepcopy(map)
    temp[row][col] = value

    # # check in row
    # for i in range(9):
    #     t = get_available_number(map, i, col)
    #     if ((len(t) == 1) and t[0] == value and (i != row)) or ((map[row][i] == value)):
    #         return False
    # # check in col
    # for i in range(9):
    #     t = get_available_number(map, row, i)
    #     if ((len(t) == 1) and t[0] == value and (i != col)) or ((map[i][col] == value)):
    #         return False
    # # check in block
    # temp_row = int(row / 3) * 3
    # temp_col = int(col / 3) * 3
    # for i in range(temp_row, temp_row + 3):
    #     for j in range(temp_col, temp_col + 3):
    #         t = get_available_number(map, i, j)
    #         if ((len(t) == 1) and t[0] == value and (i != row) and (j != col)) or ((map[i][j] == value)):
    #             return False

    # check in row
    for i in range(9):
        if (map[row][i] == value) and (i != col):
            return False
    # check in col
    for i in range(9):
        if (map[i][col] == value) and (i != row):
            return False
    # check in block
    temp_row = int(row / 3) * 3
    temp_col = int(col / 3) * 3
    for i in range(temp_row, temp_row + 3):
        for j in range(temp_col, temp_col + 3):
            if (map[i][j] == value) and (i != row) and (j != col):
                return False

    # judge
    # row
    row_rest = []
    row_count = 0
    for i in range(9):
        if temp[row][i] == 0:
            row_count += 1
            row_rest = list(set(get_available_number(temp, row, i)).union(set(row_rest)))
    if row_count > len(row_rest):
        return False
    # col
    col_rest = []
    col_count = 0
    for i in range(9):
        if temp[i][col] == 0:
            col_count += 1
            col_rest = list(set(get_available_number(temp, i, col)).union(set(col_rest)))
    if col_count > len(col_rest):
        return False
    # block
    block_rest = []
    block_count = 0
    temp_row = int(row / 3) * 3
    temp_col = int(col / 3) * 3
    for i in range(temp_row, temp_row + 3):
        for j in range(temp_col, temp_col + 3):
            if temp[temp_row][temp_col] == 0:
                block_count += 1
                block_rest = list(set(get_available_number(temp, temp_row, temp_col)).union(set(block_rest)))
    if block_count > len(block_rest):
        return False
    return True


