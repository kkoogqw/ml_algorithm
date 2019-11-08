import numpy as np
import scipy.stats as sta

# input : Test result:
# output : the diffierent coins (A/B)

# read test result from a .txt file:

# 读取txt文件中的实验结果，以list形式进行参数传递
def read_file(file_name):
    data = np.loadtxt(file_name, dtype=int)
    data = data.tolist()
    return data

# 情况A 公式：p = p1 / (p0 + p1)
def condition_know_coin_type(test_file_name):
    test_result = read_file(test_file_name)
    # result = []
    A_coin_data = [0, 0]
    B_coin_data = [0, 0]
    for i in range(len(test_result)):
        if test_result[i][0] == 10:
            for j in range(1, len(test_result[i])):
                if test_result[i][j] == 0:
                    A_coin_data[0] += 1
                else:
                    A_coin_data[1] += 1
        if test_result[i][0] == -10:
            for j in range(1, len(test_result[i])):
                if test_result[i][j] == 0:
                    B_coin_data[0] += 1
                else:
                    B_coin_data[1] += 1

    A_result = A_coin_data[1] / (A_coin_data[0] + A_coin_data[1])
    B_result = B_coin_data[1] / (B_coin_data[0] + B_coin_data[1])
    result = [A_result, B_result]
    return result



def EM_step(test_data, last_value):
    test_data = np.array(test_data)
    A_coin_data = [0, 0]
    B_coin_data = [0, 0]
    # 上一次/初始概率参数
    A_pre = last_value[0]
    B_pre = last_value[1]

    for unit_data in test_data:
        length_unit_data = len(unit_data)
        # 实验结果中用0/1记录正反面
        h = unit_data.sum()
        t = length_unit_data - h

        # scipy -> binom
        # 二项分布模型计算
        A_con = sta.binom.pmf(h, length_unit_data, A_pre)
        B_con = sta.binom.pmf(h, length_unit_data, B_pre)

        A_pow = A_con / (A_con + B_con)
        B_pow = B_con / (A_con + B_con)
        # 期望计算
        A_coin_data[0] += A_pow * t
        A_coin_data[1] += A_pow * h
        B_coin_data[0] += B_pow * t
        B_coin_data[1] += B_pow * h

    next_A_value = A_coin_data[1] / (A_coin_data[0] + A_coin_data[1])
    next_B_value = B_coin_data[1] / (B_coin_data[0] + B_coin_data[1])
    return [next_A_value, next_B_value]

def EM_loop(test_data, init_value, loop_count):
    # 多次迭代计算

    step_result_record = [init_value]
    value = init_value
    for i in range(loop_count):
        next_value = EM_step(test_data, value)
        step_result_record.append(next_value)
        value = next_value

    return [next_value, step_result_record]


def condition_unknow_coin_type(test_file_name):
    test_result = read_file(test_file_name)
    result = EM_loop(test_result, [0.6, 0.5], 20)
    return result


def main():
    file_name_a = 'a.txt'
    file_name_b = 'b.txt'
    condition_A_result = condition_know_coin_type(file_name_a)
    condition_B_result = condition_unknow_coin_type(file_name_b)

    print("A: Maximum likeihood\n Coin A:\t", condition_A_result[0], "\n Coin B:\t", condition_A_result[1])
    print("B: Expectation maximization\n Coin A:\t", condition_B_result[0][0], "\n Coin B:\t", condition_B_result[0][1])
    print("In condition B, each EM loop result is:")
    print("Coin A\t\t\t\t Coin B")
    for i in range(len(condition_B_result[1])):
        print(condition_B_result[1][i][0], condition_B_result[1][i][1])
    return

if __name__ == '__main__':
    main()