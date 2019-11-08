#%%
import numpy as np
import pandas as pd
import os
import time

#%% import data from folder
# 导入数据集 使用自己编写的读取函数进行
import read_data
# 数据集分三种
# 1. 纯 测试集 160 test_data
# 2. 纯 训练集 240 train_data
# 3. 全部样例 400 all_data
train_data, test_data = read_data.read_dataset_by_type()

all_data = read_data.read_dataset_all()


# 将图片矩阵进行展平操作 113 * 98 -> 1 * 10304
train_data_flat = read_data.get_flat_array(train_data)
test_data_flat = read_data.get_flat_array(test_data)

all_data_flat = read_data.get_flat_array(all_data)

#%% 进行PCA降维处理计算
'''Part 1 - PCA'''

#导入自己编写的PCA计算函数库
import PCA

# 计算训练集的PCA投影矩阵 并进行保存
PCA_matrix, eig_values, eig_vectors, index = PCA.PCA_matrix(train_data_flat, 40)

print(PCA_matrix)

# 保存相关计算结果
np.savetxt("PCA_matrix.txt", PCA_matrix)

# 1. run train dataset : train_data * PCA_matrix
# train_data * PCA_matrix 计算得到(240 * 40)的训练集PCA结果与对应的因子均值
train_data_pca = np.array(np.mat(train_data_flat) * np.mat(PCA_matrix))
print(train_data_pca)
np.savetxt("train_data_pca.txt", train_data_pca)

train_data_pca_mean = train_data_pca.mean(axis=0)
print(train_data_pca_mean)
np.savetxt("train_data_pca_mean.txt", train_data_pca_mean)


# 2. run test dataset : test_data * PCA_matrix
# test_data * PCA_matrix 计算得到(240 * 40)的测试集PCA结果与对应的均值
test_data_pca = np.array(np.mat(test_data_flat) * np.mat(PCA_matrix))
print(test_data_pca)
np.savetxt("test_data_pca.txt", test_data_pca)

test_data_pca_mean = test_data_pca.mean(axis=0)
print(test_data_pca_mean)
np.savetxt("test_data_pca_mean.txt", test_data_pca_mean)


#%% 进行人脸识别与距离归类分析
'''Part 2 - Match faces'''

# 导入个人编写的求解欧氏距离/马氏距离的相关函数
import distance

# load data from part 1:
train_data_pca = np.loadtxt("train_data_pca.txt")
test_data_pca = np.loadtxt("test_data_pca.txt")


'''2-1 - Euclidean Distance'''
# 欧式距离匹配
Euclidean_match_result = distance.Euclidean_match(train_data_pca, test_data_pca)
for i in Euclidean_match_result:
    print("match label:", i[1], "\treal label:", i[0], "\tState:", (i[1] == i[0]))
print("\n")

Euclidean_match_error_count, Euclidean_match_rate = distance.check_Euclidean_match(Euclidean_match_result)
print("Error count:", Euclidean_match_error_count, "\tCorrect Ratio:", Euclidean_match_rate)
print("=================================================\n")

'''2-2 - Mahalanobis Distance'''
# 马氏距离匹配
# 计算各个类别的均值/协方差矩阵
# 由于马氏距离的计算特点，只取前4个图像维度进行。
train_m_d = distance.get_Mahalanobis_distance_matrix(train_data_pca, True)
test_m_d = distance.get_Mahalanobis_distance_matrix(test_data_pca, False)

train_cov_list = []
train_mean_list = []
for i in range(len(train_m_d)):
    train_cov_list.append(np.array(pd.DataFrame(train_m_d[i]).cov()))
    train_mean_list.append(np.mean(train_m_d[i], axis=0))

# 进行最近马氏距离匹配
m_d_re = distance.Mahalanobis_distance(test_m_d, train_cov_list, train_mean_list, 40)
for i in m_d_re:
    print("match label:", i[1], "\treal label:", i[0], "\tState:", (i[1] == i[0]))
print("\n")
# 统计错误个数与准确率
Mahalanobis_match_error, Mahalanobis_match_rate = distance.check_Mahalanbis_match(m_d_re)
print("Error count:", Mahalanobis_match_error, "\tCorrect Ratio:", Mahalanobis_match_rate)
print("=================================================\n")



#%%
'''Part 3 - K-means'''

# 导入自己编写的K-means计算函数库
import k_means

# 按照所有总体(400 samples)计算PCA投影矩阵 并保存
all_PCA_matrix, all_eig_values, all_eig_vectors, all_index = PCA.PCA_matrix(all_data_flat, 40)
print(all_PCA_matrix)

np.savetxt("all_PCA_matrix.txt", all_PCA_matrix)

# 计算PCA投影矩阵与元数据矩阵的乘积 得到降维数据
# 保存 降维结果/均值结果

all_data_pca = np.array(np.mat(all_data_flat) * np.mat(all_PCA_matrix))
print(all_data_pca)
np.savetxt("all_data_pca.txt", all_data_pca)

all_data_pca_mean = all_data_pca.mean(axis=0)
print(all_data_pca_mean)
np.savetxt("all_data_pca_mean.txt", all_data_pca_mean)

# Load data from pre-calculation
all_data_pca = np.loadtxt("all_data_pca.txt")

pca_data = k_means.init_dataset(all_data_pca)
no_pca_data = k_means.init_dataset(all_data_flat)

# Before PCA (400 * 10304)
# 未进行降维处理的结果进行k-means聚类
no_pca_centroids, no_pca_cluster_result, no_pca_loop_count = k_means.k_means(no_pca_data, 40)
no_pca_k_means_result, no_pca_k_means_accuracy = k_means.get_accuracy(no_pca_data, 40, no_pca_cluster_result)
k_means.print_k_means_result_detail(no_pca_k_means_result, 40)

print("The k-means accuracy of ATT-FACES dataset without PCA is:\t", no_pca_k_means_accuracy)

# After PCA (400 * 40)
# 经过PCA降维处理后的数据进行PCA降维处理
pca_centroids, pca_cluster_result, pca_loop_count = k_means.k_means(pca_data, 40)
pca_k_means_result, pca_k_means_accuracy = k_means.get_accuracy(pca_data, 40, pca_cluster_result)
k_means.print_k_means_result_detail(pca_k_means_result, 40)

print("The k-means accuracy of ATT-FACES dataset with PCA is:\t", pca_k_means_accuracy)



