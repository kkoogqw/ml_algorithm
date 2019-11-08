#%%
import numpy as np
import pandas as pd

#%%
def data_std(data):
    temp = pd.DataFrame(data)
    mean = temp.mean()
    std = temp.std()

    for i in temp:
        temp[i] = temp[i] - mean[i]
        # temp[i] = temp[i] / std[i]

    return temp

def get_cov_matrix(std_data):
    return std_data.cov()


def get_eigendata(cov_matrix):
    eig_values, eig_vectors = np.linalg.eig(cov_matrix)
    return eig_values, eig_vectors


def PCA_matrix(data_matrix, dest_dim):

    # flat_data = read_data.get_flat_array(data_matrix)
    std_data = data_std(data_matrix)
    cov_matrix = get_cov_matrix(std_data)
    eig_values, eig_vectors = get_eigendata(cov_matrix)
    print("get the eigenvalues & eigenvectors")

    eig_values = np.real(eig_values)
    eig_vectors = np.real(eig_vectors)

    sorted_eig_values = -np.sort(-eig_values)

    index = []
    for i in range(len(sorted_eig_values)):
        for j in range(len(eig_values)):
            if sorted_eig_values[i] == eig_values[j]:
                index.append(j)
                break
            else:
                continue
        if len(index) >= dest_dim:
            break

    temp = (eig_vectors[index])
    PCA_matrix = temp.T

    return PCA_matrix, eig_values, eig_vectors, index
