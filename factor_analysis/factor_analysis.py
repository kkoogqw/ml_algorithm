import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

#%%
# import dataset and set labels
x_label = {"x0": "城市",
           "x1": "非衣业人口数",
           "x2": "工业总产值",
           "x3": "货运总量",
           "x4": "批发零售住宿餐饮从业人数",
           "x5": "地方政府预算内收入",
           "x6": "城乡居民年底储蓄余额",
           "x7": "在岗职工人数",
           "x8": "在岗职工工资总额",
           "x9": "人均居住面积",
           "x10": "每万人拥有公共汽车数",
           "x11": "人均拥有铺装道路面积",
           "x12": "人均公共绿地面积", }

data = pd.read_excel("6-3.xls", index_col="Cities")

print(data)

#%%
# trans to np.array type
matrix_data = data.values
print(matrix_data)

#%%
# data -> std data(org data - mean)/(std);
# 数据标准化处理 (data-均值)/(标准差)

factors = ["x1", "x2", "x3", "x4", "x5", "x6", "x7","x8", "x9", "x10", "x11", "x12"]

mean_vector = data.mean()
std_vector = data.std()

std_data = data

for i in range(len(factors)):
    std_data[factors[i]] = data[factors[i]].map(lambda x: x - mean_vector[i])
    std_data[factors[i]] = data[factors[i]].map(lambda x: x / std_vector[i])

#%%
# using sklearn - PCA method get do pca
# 使用库函数计算PCA

m_list = [3, 4, 5]

pca = PCA(n_components=12)
pca.fit(std_data)
pca_result = pca.transform(std_data)

#%%
Variance_ratio = pca.explained_variance_ratio_
Total = pca.explained_variance_
eig_vector = pca.components_

print("Variance:\n", Variance_ratio)
print("eigenvalue:\n", Total)
print("eigenvector:\n", eig_vector)

#%%
Cumulative = []
temp = 0
for i in range(len(Variance_ratio)):
    temp += Variance_ratio[i]
    Cumulative.append(round(temp, 8))
Cumulative = np.array(Cumulative)

#%% make table

table = pd.DataFrame([Total, Variance_ratio, Cumulative]).T
table.columns = ["Total", "Variance", "Cumulative"]
table.index = range(1,13)

print(table)
table.to_excel("Record/Total Variance Explained.xls")

#%% make graph
plt.figure()
x = range(1, 13)
y = Total

plt.xlabel("Component Number")
plt.xticks(range(1, 13))

plt.ylabel("Eugenvalue")
plt.yticks(range(0, int(max(Total)) + 1))

plt.title("Scree Plot")
plt.plot(x, y, marker='o')

plt.savefig("Record/Scree Plot.jpg")
plt.show()

#%% build Component Matrix

component_matrix = []
vec = eig_vector
print(vec)
for i in range(len(Total)):
    component_matrix.append(np.sqrt(Total[i]) * vec[i])

component_matrix = pd.DataFrame(np.array(component_matrix).T)
component_matrix.columns = [k for k in range(1, 13)]
component_matrix.index = factors

for j in range(len(m_list)):
    temp = [k for k in range(1, m_list[j] + 1)]
    temp_component_matrix = (component_matrix[temp])
    print(temp_component_matrix)
    temp_component_matrix.to_excel("Record/Component Matrix m_" + str(m_list[j]) + ".xls")





########################################################################################################################
'''
下面是个人计算测试特征向量和特征值时用到的PCA算法步骤，作为参考。
为了更好的性能和精度，实验中没有采用自己编写的PCA算法，这里只是为了计算特征值/向量用到的
根据计算，同样采用标准化后的数据(（数据-均值）/ 标准差)得到的特征向量和特征值相同。
同时，这里采用数据的相关系数进行计算（由于各个指标的单位开始并没有统一）
但是经过标准化后的数据相关系数矩阵和协方差矩阵的特征值与特征向量是相同的，这一点在后面的计算中可以看到。
'''
'''My PCA porcess: '''
# 自己使用的PCA计算方法
#%%
# get cov & corr matrix

cov_matrix = std_data.cov()
corr_matrix = std_data.corr()

print(std_data)
print(cov_matrix)
print(corr_matrix)

#%%
# get eigenvalue and eigenvector
# 计算特征值 & 特征向量

corr_eigenvalue, corr_eigenvector =  np.linalg.eig(corr_matrix)

print(corr_eigenvalue)
print(corr_eigenvector)

#%%
# sort the eigenvalues
# 对特征值排序,取得较大特征值对应的特征向量

corr_sorted_eigenvalue = corr_eigenvalue.tolist()
corr_sorted_eigenvalue.sort(reverse=True)
corr_sorted_eigenvalue = np.array(corr_sorted_eigenvalue)

corr_sorted_eigenvector = []

index = []
for i in range(len(corr_sorted_eigenvalue)):
    for j in range(len(corr_eigenvalue)):
        if corr_sorted_eigenvalue[i] == corr_eigenvalue[j]:
            index.append(j)

for i in range(len(index)):
    corr_sorted_eigenvector.append(corr_eigenvector[index[i]])



