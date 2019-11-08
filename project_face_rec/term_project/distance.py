#%%
import numpy as np
import read_data

def get_distance(distance_type, point1, point2):
    if distance_type == "E":
        return np.sqrt(np.sum(np.square(point1 - point2)))

    elif distance_type == "M":
        X = np.vstack([point1, point2])
        print(X)
        X_t = X.T
        print(X_t)
        cov = np.cov(X)
        print(cov)
        cov_inverse = cov.I
        print(cov_inverse)

        n = X_t.shape[0]
        result = []
        for i in range(0, n):
            for j in range(i + 1, n):
                delta = X_t[i] - X_t[j]
                d = np.sqrt(np.dot(np.dot(delta, cov_inverse), delta.T))
                result.append(d)

        print(result)

        return np.array(result)
    else:
        return "ERROR type distance!"


def Euclidean_match(train_data, test_data):
    result = []
    for i in range(len(test_data)):
        label = 0
        min_dis = 0
        dis = []
        for j in range(len(train_data)):
            dis.append(get_distance("E", test_data[i], train_data[j]))
        min_dis = min(dis)
        m_dis = np.array(dis)
        match_label = np.argwhere(dis == min_dis)[0][0]
        label = read_data.get_label(i, False)
        result.append([label, match_label, min_dis, dis])

    for sample in result:
        sample[1] = read_data.get_label(sample[1], True)
    return result

def check_Euclidean_match(match_result):
    error_count = 0
    for i in range(len(match_result)):
        label = match_result[i][0]
        match_label = match_result[i][1]
        if label != match_label:
            error_count += 1
    return error_count, (1 - (error_count/len(match_result)))


def get_Mahalanobis_distance_matrix(PCA_data, data_type):
    #%% train data
    if data_type == True:
        matrix_list = []
        t = 0
        while t < 240:
            m = PCA_data[t:t + 6, 0:4]
            t = t + 6
            matrix_list.append(m)
        return matrix_list
    # %% test data
    else:
        matrix_list = []
        t = 0
        while t < 160:
            m = PCA_data[t, 0:4]
            t = t + 1
            matrix_list.append(m)
        return matrix_list


def Mahalanobis_distance(test_dataset, cov_list, mean_list, factor_count):
    result = []
    m_d = []
    for i in range(len(test_dataset)):
        dis = []
        for j in range(factor_count):
            d = np.sqrt(np.mat(test_dataset[i] - mean_list[j]) *
                        np.mat(cov_list[j]).I *
                        np.mat(test_dataset[i] - mean_list[j]).T)
            dis.append(d.tolist()[0][0])
        m_d.append(np.array(dis))

    for i in range(len(m_d)):
        min_dis = np.min(m_d[i])
        match_label = np.argwhere(m_d[i] == min_dis)[0][0] + 1
        real_label = read_data.get_label(i, False)
        result.append([real_label, match_label, min_dis, m_d[i]])

    return result

def check_Mahalanbis_match(match_result):
    error_count = 0
    for i in range(len(match_result)):
        label = match_result[i][0]
        match_label = match_result[i][1]
        if label != match_label:
            error_count += 1
    return error_count, (1 - (error_count/len(match_result)))