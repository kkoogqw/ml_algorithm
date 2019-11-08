# function & lib import
import numpy as np
import struct
import random
import copy as cp


class MNIST_image:
    def __init__(self, data_matrix, data_label):
        self.data = data_matrix
        self.label = data_label


def get_data_from_dataset(data_path, label_path):
    with open(data_path, "rb") as temp1:
        image_data = temp1.read()
    with open(label_path, "rb") as temp2:
        label_data = temp2.read()

    images = []
    image_index = 0
    image_index += struct.calcsize(">IIII")
    for i in range(60000):
        tmp = struct.unpack_from(">784B", image_data, image_index)
        images.append(np.reshape(tmp, (28, 28)))
        image_index += struct.calcsize(">784B")

    label_index = 0
    label_index += struct.calcsize(">II")
    labels = struct.unpack_from(">60000B", label_data, label_index)

    images = np.array(images)
    labels = np.array(labels)
    dataset = []

    if len(images) == len(labels):
        for i in range(len(images)):
            temp = MNIST_image(images[i], labels[i])
            dataset.append(temp)
    return dataset



def get_distance(distance_type, point1, point2):
    if distance_type == "E":
        return np.sqrt(np.sum(np.square(point1 - point2)))
    elif distance_type == "M":
        return np.sum(np.abs(point1 - point2))
    elif distance_type == "C":
        return np.abs(point1 - point2).max()

def set_centroids(dataset, k, type_number):
    # type info:
    # 1. get random 10 labels from 0~59999 as centroids
    # 2. get the first 10 labels as centroids
    # 3. choose 1~10 label from dataset as centroids
    if type_number == "R":
        temp_list = np.arange(len(dataset)).tolist()
        index = random.sample(temp_list, k)
        centroids = []
        for i in range(len(index)):
            centroids.append(dataset[index[i]].data)
        return centroids, index

    elif type_number == "O":
        index = np.arange(k).tolist()
        centroids = []
        for i in range(len(index)):
            centroids.append(dataset[index[i]].data)
        return centroids, index

    elif type_number == "N":
        index = []
        label_list = []
        for i in range(len(dataset)):
            if len(index) == 10 or len(label_list) == 10:
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
    result = cp.deepcopy(matrix_list[0])
    for i in range(1, len(matrix_list)):
        result += matrix_list[i]
    return result / len(matrix_list)

def k_means(dataset, k_value, distance_type, centroids_init_type):
    sample_count = len(dataset)
    is_centroids_changed = True
    # set the start centroids
    centroids, centroids_index = set_centroids(dataset, k_value, centroids_init_type)

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
            min_distance = get_distance(distance_type, dataset[i].data, centroids[0])
            min_cluster_index = 0

            for j in range(k_value):
                temp_distance = get_distance(distance_type, dataset[i].data, centroids[j])
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
              "\tk-means label:", k_means_result[i][3],
              "\tk-means accuracy for a group:", k_means_result[i][5])



def run():
    data_path = "dataset/train-images.idx3-ubyte"
    label_path = "dataset/train-labels.idx1-ubyte"

    MNIST_dataset = get_data_from_dataset(data_path, label_path)

    # 定义不同的距离计算类型 测试准确率
    Euclidean_distance = "E" # 欧氏距离
    Manhattan_distance = "M" # 曼哈顿距离
    Chebyshev_distance = "C" # 切比雪夫距离

    # 定义聚类中心选取方法
    random_centroids_type = "R" # 随机从60000个样例中选取10个初始聚点中心
    label_centroids_type = "N"  # 按照样例标签选取0~9 共10个初始聚点中心
    order_centroids_type = "O"  # 选取数据集前10个样例作为初始聚点中心

    # 定义k值
    K_value = 10

    # 欧式距离 - 标签初始聚类中心
    test1_centroids, test1_cluster_result, test1_loop = k_means(MNIST_dataset,
                                                                K_value,
                                                                Euclidean_distance,
                                                                label_centroids_type)
    test1_result, test1_accuracy = get_accuracy(MNIST_dataset,
                                                K_value,
                                                test1_cluster_result)

    # 欧式距离 - 随机初始聚类中心
    test2_centroids, test2_cluster_result, test2_loop = k_means(MNIST_dataset,
                                                                K_value,
                                                                Euclidean_distance,
                                                                random_centroids_type)
    test2_result, test2_accuracy = get_accuracy(MNIST_dataset,
                                                K_value,
                                                test2_cluster_result)

    # 欧式距离 - 前10样例初始聚类中心
    test3_centroids, test3_cluster_result, test3_loop = k_means(MNIST_dataset,
                                                                K_value,
                                                                Euclidean_distance,
                                                                order_centroids_type)
    test3_result, test3_accuracy = get_accuracy(MNIST_dataset,
                                                K_value,
                                                test3_cluster_result)

    # 曼哈顿距离 - 标签初始聚类中心
    test4_centroids, test4_cluster_result, test4_loop = k_means(MNIST_dataset,
                                                                K_value,
                                                                Manhattan_distance,
                                                                label_centroids_type)
    test4_result, test4_accuracy = get_accuracy(MNIST_dataset,
                                                K_value,
                                                test4_cluster_result)

    test5_centroids, test5_cluster_result, test5_loop = k_means(MNIST_dataset,
                                                                K_value,
                                                                Chebyshev_distance,
                                                                label_centroids_type)
    test5_result, test5_accuracy = get_accuracy(MNIST_dataset,
                                                K_value,
                                                test5_cluster_result)

    print("Euclidean distance / 0~9 label for initial center:",
          "\nAccuracy:\t", test1_accuracy,
          "\nloop count:\t", test1_loop)
    print_k_means_result_detail(test1_result, K_value)
    print("==============================================================================")


    print("Euclidean distance / Random for initial center:",
          "\nAccuracy:\t", test2_accuracy,
          "\nloop count:\t", test2_loop)
    print_k_means_result_detail(test2_result, K_value)
    print("==============================================================================")

    print("Euclidean distance / First 10 samples for initial center:",
          "\nAccuracy:\t", test3_accuracy,
          "\nloop count:\t", test3_loop)
    print_k_means_result_detail(test3_result, K_value)
    print("==============================================================================")

    print("Manhattan distance / 0~9 label for initial center:",
          "\nAccuracy:\t", test4_accuracy,
          "\nloop count:\t", test4_loop)
    print_k_means_result_detail(test4_result, K_value)
    print("==============================================================================")

    print("Chebyshev distance / 0~9 label for initial center:",
          "\nAccuracy:\t", test5_accuracy,
          "\nloop count:\t", test5_loop)
    print_k_means_result_detail(test5_result, K_value)
    print("==============================================================================")


if __name__ == '__main__':
    run()


