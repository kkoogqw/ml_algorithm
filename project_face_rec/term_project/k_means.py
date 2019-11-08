# function & lib import
import numpy as np
import copy as cp

import distance

class face_image:
    def __init__(self, data_array, data_index):
        self.data = data_array
        self.label = int((data_index / 10)) + 1

def init_dataset(data):
    data_list = []
    for i in range(len(data)):
        temp = face_image(data[i], i)
        data_list.append(temp)
    return  data_list

def set_centroids(dataset, factor_count):
    index = []
    label_list = []
    for i in range(len(dataset)):
        if len(index) == factor_count or len(label_list) == factor_count:
            break
        else:
            if dataset[i].label in label_list:
                continue
            else:
                label_list.append(dataset[i].label)
                index.append(i)
    centroids = []
    for i in range(len(index)):
        centroids.append(dataset[index[i]].data)
    return centroids, index


def get_matrix_mean(matrix_list):
    return np.mean(np.array(matrix_list), axis=0)

def k_means(dataset, k_value):
    sample_count = len(dataset)
    is_centroids_changed = True
    # set the start centroids
    centroids, centroids_index = set_centroids(dataset, k_value)

    cluster_result = np.zeros(sample_count, dtype=int).tolist()
    centroids_change_record = []
    centroids_change_record.append(centroids)
    loop_count = 0
    while is_centroids_changed == True:
        loop_count += 1
        print("Loop :", loop_count)
        is_centroids_changed = False
        # calculate the min distance to the every centroids
        for i in range(sample_count):
            min_distance = distance.get_distance("E", dataset[i].data, centroids[0])
            min_cluster_index = 0

            for j in range(k_value):
                temp_distance = distance.get_distance("E", dataset[i].data, centroids[j])
                if min_distance > temp_distance:
                    min_distance = temp_distance
                    min_cluster_index = j

            # refresh the cluster
            if cluster_result[i] != min_cluster_index:
                is_centroids_changed = True
                cluster_result[i] = min_cluster_index

        # refresh the centorid
        for m in range(k_value):
            temp_cluster = []
            for n in range(sample_count):
                if cluster_result[n] == m:
                    temp_cluster.append(dataset[n].data)
            # temp_cluster = np.array(temp_cluster)
            new_centroid = get_matrix_mean(temp_cluster)
            centroids[m] = new_centroid

    return centroids, cluster_result, loop_count


def get_accuracy(dataset, k_value, result):
    k_means_result = []
    for i in range(k_value):
        k_means_result.append([i, [], [], -1, -1, -1])

    for j in range(len(result)):
        k_means_result[result[j]][1].append(j)
        k_means_result[result[j]][2].append(dataset[j].label)

    for k in range(k_value):
        temp_label = np.array(k_means_result[k][2])
        labels_counts = np.bincount(temp_label)
        k_means_result[k][3] = np.argmax(labels_counts)

    for m in range(k_value):
        error_count = 0
        for n in range(len(k_means_result[m][2])):
            if k_means_result[m][2][n] != k_means_result[m][3]:
                error_count += 1
        k_means_result[m][4] = error_count
        k_means_result[m][5] = 1 - (error_count / len(k_means_result[m][2]))

    totle_error = 0
    for p in range(k_value):
        totle_error += k_means_result[p][4]
    print(totle_error)
    accuracy = 1 - (totle_error / len(dataset))

    return k_means_result, accuracy

def print_k_means_result_detail(k_means_result, k_value):
    for i in range(k_value):
        print("Group:", k_means_result[i][0],
              "\treal label:", k_means_result[i][3],
              "\tk-means accuracy for a group:", k_means_result[i][5])

