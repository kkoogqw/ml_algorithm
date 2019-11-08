#%%
import numpy as np
import pandas as pd

'''
数据处理部分

0. 数据格式化为可计算形式
1. 均值
2. 协方差
'''
#%% import data
# 数据导入，设置行标签
train_data = pd.read_csv("train.txt", names=["buying", "maint", "doors", "persons", "lug boot", "safety", "type"])
test_data  = pd.read_csv("test.txt", names=["buying", "maint", "doors", "persons", "lug boot", "safety"])
# 删除存在BUG的数据列 "Safety"
train_data.drop(columns=["safety"], axis=1, inplace=True)
test_data.drop(columns=["safety"], axis=1, inplace=True)
# 定义各个指标的标准化值/文本数据 -> 数字
buying = {"low":0, "med":1, "high":2, "vhigh":4}
maint = {"low":0, "med":1, "high":2, "vhigh":4}
doors = {"2":0, "3":1, "4":2, "5more":3}
persons = {"2":0, "4":1, "more":2}
lug_boot = {"small":0, "med":1, "big":2}

# 训练集/测试集数据替换(标准格式化，使之可以进行矩阵的计算)
#%% train data operation
train_data["maint"] = train_data["maint"].replace(maint)
train_data["buying"] = train_data["buying"].replace(buying)
train_data["doors"] = train_data["doors"].replace(doors)
train_data["persons"] = train_data["persons"].replace(persons)
train_data["lug boot"] = train_data["lug boot"].replace(lug_boot)

#%% test data operation
test_data["maint"] = test_data["maint"].replace(maint)
test_data["buying"] = test_data["buying"].replace(buying)
test_data["doors"] = test_data["doors"].replace(doors)
test_data["persons"] = test_data["persons"].replace(persons)
test_data["lug boot"] = test_data["lug boot"].replace(lug_boot)

#%% train data build type
# 训练集数据分组(按照4种类型进行)
unacc_type = train_data[train_data.type == "unacc"]
acc_type = train_data[train_data.type == "acc"]
good_type = train_data[train_data.type == "good"]
vgood_type = train_data[train_data.type == "vgood"]
# 分类完成后，删除类别标签一栏，只保留可以计算的数据
unacc_type.drop(columns=["type"], axis=1, inplace=True)
acc_type.drop(columns=["type"], axis=1, inplace=True)
good_type.drop(columns=["type"], axis=1, inplace=True)
vgood_type.drop(columns=["type"], axis=1, inplace=True)

#%% get type mean
# 获取各类别的均值向量表
unacc_mean = unacc_type.mean()
acc_mean = acc_type.mean()
good_mean = good_type.mean()
vgood_mean = vgood_type.mean()
# 将dataframe类型转换为np.matrix,方便进行下一步计算
unacc_mean = np.mat(unacc_mean)
acc_mean = np.mat(acc_mean)
good_mean = np.mat(good_mean)
vgood_mean = np.mat(vgood_mean)

print("unacc\t", unacc_mean)
print("acc\t\t", acc_mean)
print("good\t", good_mean)
print("vgood\t", vgood_mean)

#%% get cov matrix
# 计算各个类别的协方差矩阵，处理方式与均值向量相同
unacc_cov = unacc_type.cov().values
acc_cov = acc_type.cov().values
good_cov = good_type.cov().values
vgood_cov = vgood_type.cov().values

unacc_cov = np.mat(unacc_cov)
acc_cov = np.mat(acc_cov)
good_cov = np.mat(good_cov)
vgood_cov = np.mat(vgood_cov)

print("unacc\n", unacc_cov)
print("acc\n", acc_cov)
print("good\n", good_cov)
print("vgood\n", vgood_cov)

#%%
print(good_mean)
print(good_mean.T)

#%% data summary
# 构造列表，对均值/协方差矩阵进行整理
cov_matrix = [unacc_cov, acc_cov, good_cov, vgood_cov]
average_list = [unacc_mean, acc_mean, good_mean, vgood_mean]

#%% classes dictionary
# 类别编号声明，方便进行归类处理
classes = {0:"unacc", 1:"acc", 2:"good", 3:"vgood"}
type_count = 4

'''
距离分析函数定义

run_distinct_cov(test_dataset, cov_list, mean_list, type_count)                     -> 协方差不同情况下进行计算距离(判别值)

do_distinct_cov_classify(result, classes)                                           -> 协方差不同进行类别划分

run_same_cov(test_dataset, cov_list, mean_list, type_count, traindata_size)         -> 协方差相同计算判别值

do_same_cov_classif(result)                                                         -> 协方差相同进行类别划分
'''
#%%
# diffierent cov
# W_ij = [(x - μ_i)' * cov_inverse * (x - μ_i)] - [(x - μ_j)' * cov_inverse * (x - μ_j)]
def run_distinct_cov(test_dataset, cov_list, mean_list, type_count):
    cov_sample_result = []
    for line in range(test_dataset.shape[0]):
        x = test_dataset.iloc[line].values
        i_result = []
        for i in range(type_count):
            j_result = []
            for j in range(type_count):
                if i != j:
                    a = ((x - mean_list[i]) * (cov_list[i].I) * ((x - mean_list[i]).T))
                    b = ((x - mean_list[j]) * (cov_list[j].I) * ((x - mean_list[j]).T))
                    W_ij = a - b
                    temp = [i, j, sum(W_ij.tolist(), [])[0]]
                    print(i, j, sum(W_ij.tolist(), [])[0])
                    j_result.append(temp)
            i_result.append(j_result)
        cov_sample_result.append(i_result)
        print("=========================")
    return cov_sample_result

# W_ij < 0(i != j) => sample in Class i
def do_distinct_cov_classify(result, classes):
    cov_predict_result = []
    for sample in result:
        # print(sample)
        for j in sample:
            # print(j)
            if j[0][2] < 0 and j[1][2] < 0 and j[2][2] < 0:
                cov_predict_result.append(classes[j[0][0]])
                break
            if j[0][0] == 3:
                cov_predict_result.append("None")
            else:
                continue
    return  cov_predict_result

# same cov-matrix
# W_ij = [(x - (μ_i + μ_j)/2) * cov_inverse * (μ_i - μ_j)]
def run_same_cov(test_dataset, cov_list, mean_list, type_count, traindata_size):
    # cov = (1/(n-k))*(sum(cov_matrix))
    sig_cov = (1 / (traindata_size - 4)) * sum(cov_list)
    uncov_sample_result = []
    for line in range(test_dataset.shape[0]):
        x = test_dataset.iloc[line].values
        i_result = []
        for i in range(type_count):
            j_result = []
            for j in range(type_count):
                if i != j:
                    W_ij = (x - (mean_list[i] + mean_list[j]) / 2) * sig_cov.I * (
                                mean_list[i] - mean_list[j]).T
                    temp = [i, j, sum(W_ij.tolist(), [])[0]]
                    print(i, j, sum(W_ij.tolist(), [])[0])
                    j_result.append(temp)
            i_result.append(j_result)
        uncov_sample_result.append(i_result)
        print("=========================")
    return  uncov_sample_result

# W_ij > 0(i != j) => sample in Class i
def do_same_cov_classif(result, classes):
    uncov_predict_result = []
    for sample in result:
        # print(sample)
        for j in sample:
            # print(j)
            if j[0][2] > 0 and j[1][2] > 0 and j[2][2] > 0:
                uncov_predict_result.append(classes[j[0][0]])
                break
            if j[0][0] == 3:
                uncov_predict_result.append("None")
            else:
                continue
    return  uncov_predict_result


# run result
#%%
distinct_W = run_distinct_cov(test_data, cov_matrix, average_list, type_count)
re1 = do_distinct_cov_classify(distinct_W, classes)
print(re1)

#%%
same_W = run_same_cov(test_data, cov_matrix, average_list, type_count, train_data.shape[0])
re2 = do_same_cov_classif(same_W, classes)
print(re2)

#%%
count = 0
for i in range(len(re1)):
    if re1[i] == re2[i]:
        count += 1
print(count)