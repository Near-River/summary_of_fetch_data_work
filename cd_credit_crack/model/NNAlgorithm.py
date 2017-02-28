#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Nate_River'

import time
import numpy as np
import functools
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

file_path = '../doc/identify.txt'
Operator_Map = {
    '＋': 0, '加': 1,
    '－': 2, '减': 3,
    '×': 4, '乘': 5
}

Number_Map = {
    '1': 0, '一': 1, '壹': 2,
    '2': 3, '二': 4, '贰': 5,
    '3': 6, '三': 7, '叁': 8,
    '4': 9, '四': 10, '肆': 11,
    '5': 12, '五': 13, '伍': 14,
    '6': 15, '六': 16, '陆': 17,
    '7': 18, '七': 19, '柒': 20,
    '8': 21, '八': 22, '捌': 23,
    '9': 24, '九': 25, '玖': 26,
    '?': 27
}


def load_operator_labels(size):
    labels = np.zeros((size, 6), dtype=float)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(size):
            line = lines[i].strip()
            c = line.split(' ')[1]
            idx = Operator_Map[c]
            temp = np.zeros((6,))
            temp[idx] = 1
            labels[i, :] = temp.transpose()
            # print(labels, labels.dtype)
    return labels


def load_number_labels(size):
    labels = np.zeros((2 * size, 29), dtype=float)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(size):
            line = lines[i].strip()
            c1, c2 = line.split(' ')[0], line.split(' ')[2]
            idx1, idx2 = Number_Map[c1], Number_Map[c2]
            temp1, temp2 = np.zeros((29,)), np.zeros((29,))
            temp1[idx1] = 1
            temp2[idx2] = 1
            labels[i, :] = temp1.transpose()
            labels[i + size, :] = temp2.transpose()
    return labels


def time_counting(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        ret = func(*args, **kwargs)
        t2 = time.time()
        print('Build classifier cost: %f' % (t2 - t1))
        return ret

    return wrapper


@time_counting
def NN_Algorithm(dataX, labelY):
    pca = PCA(n_components=200)
    _pca = pca.fit(dataX)
    dataX = _pca.transform(dataX)
    # print(dataX.shape)  # 降维后的数据维度
    m, d = dataX.shape  # 训练样本数， 输入神经元个数
    clf = MLPClassifier(solver='lbfgs', alpha=1e-3,
                        hidden_layer_sizes=(2 * d,), random_state=1)
    clf.fit(dataX, labelY)
    return _pca, clf
