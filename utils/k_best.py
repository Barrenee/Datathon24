import numpy as np


def(matrix, k):
    '''Returns the k best groups to merge with the given group'''
    best_groups = []
    for group in matrix:
        best_groups.append(sorted(matrix[group], key=lambda x: len(matrix[x]))[:k])
    return best_groups


def matrix2np(matrix):
    '''Converts the matrix to a numpy array'''
    np_matrix = np.zeros((len(matrix), len(matrix)))
    for i, group in enumerate(matrix):
        for j, group2 in enumerate(matrix[group]):
            np_matrix[i][j] = len(matrix[group2])
    return np_matrix