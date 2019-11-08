#%%
import numpy as np
from PIL import Image


#%%
def read_dataset_by_type():
    train_data = []
    test_data = []
    for i in range(40):
        folder_path = "att_faces/s"
        folder_path += (str(i + 1) + "/")
        person_train_list = []
        person_test_list = []
        for j in range(0, 6):
            file_path = folder_path + str(j + 1) + ".pgm"
            # print(file_path, "train")
            temp_im = Image.open(file_path)
            image_matrix = np.array(temp_im)
            person_train_list.append(image_matrix)
        train_data.append(person_train_list)

        for k in range(6, 10):
            file_path = folder_path + str(k + 1) + ".pgm"
            # print(file_path, "test")
            temp_im = Image.open(file_path)
            image_matrix = np.array(temp_im)
            person_test_list.append(image_matrix)
        test_data.append(person_test_list)

    return train_data, test_data

def read_dataset_all():
    all_data = []
    for i in range(40):
        folder_path = "att_faces/s"
        folder_path += (str(i + 1) + "/")
        person_train_list = []
        person_test_list = []
        for j in range(10):
            file_path = folder_path + str(j + 1) + ".pgm"
            # print(file_path, "train")
            temp_im = Image.open(file_path)
            image_matrix = np.array(temp_im)
            person_train_list.append(image_matrix)
        all_data.append(person_train_list)

    return all_data


def get_flat_array(data):
    flat_data = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            flat_data.append(data[i][j].ravel())

    flat_data = np.array(flat_data)
    return flat_data


def get_label(num, data_type):
    # For train data
    if data_type == True:
        if num >= 0 and num < 240:
            return int(num / 6) + 1
        else:
            return "ERROR index!"
    else:
        if num >= 0 and num < 160:
            return int(num / 4) + 1
        else:
            return "ERROR index!"

