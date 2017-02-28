# -*- coding: utf-8 -*-

"""
使用神经网络算法，构建模型识别图片中的字符
"""

__author__ = 'Nate_River'

import os
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from model.NNAlgorithm import *


class ModelFactory(object):
    def __init__(self):
        self.raw_data = self.load_data()
        self.operator_pca, self.operator_clf = self.get_operator_classifier()
        self.num_pca, self.num_clf = self.get_number_classifier()

    def load_data(self):
        raw_data = []
        temp_dir = os.path.abspath('../imgs')
        size = len(os.listdir(temp_dir))
        size = 500
        for i in range(1, size + 1):
            file_path = os.path.join(temp_dir, 'verifCodePic' + str(i) + '.jpg')
            img = ndimage.imread(file_path)
            # print(img.shape, img.dtype)  # (28, 90, 3)
            part_imgs = []
            for j in range(3):
                _img = img[:, 20 * j:20 * (j + 1), :]
                # print(type(_img), _img.shape)  # (28, 20, 3)
                part_imgs.append(_img)
                # subPlot = plt.subplot(1, 3, i + 1)
                # subPlot.imshow(_img)
            _img = img[:, 72:, :]  # 结果图片
            part_imgs.append(_img)
            # plt.show()
            raw_data.append(part_imgs)
        return raw_data

    def get_operator_classifier(self):
        data = self.raw_data[:]
        size = data[0][1].shape

        _X = np.zeros((len(data), *size))
        for i in range(len(data)): _X[i, :] = data[i][1]
        # print(_X.shape)  # (m, 28, 20, 3)
        t, _product = _X.shape, 1
        for i in range(1, len(t)): _product *= t[i]
        X = _X.reshape((_X.shape[0], _product))
        y = load_operator_labels(size=len(data))
        # print(X.shape, y.shape)  # (m, 1680) (m, 6)

        clf = NN_Algorithm(dataX=X, labelY=y)
        return clf

    def get_number_classifier(self):
        data = self.raw_data[:]
        size = data[0][1].shape

        _X = np.zeros((2 * len(data), *size))
        for i in range(len(data)): _X[i, :] = data[i][0]
        for i in range(len(data)): _X[i + len(data), :] = data[i][2]
        # print(_X.shape)  # (2*m, 28, 20, 3)
        t, _product = _X.shape, 1
        for i in range(1, len(t)): _product *= t[i]
        X = _X.reshape((_X.shape[0], _product))

        y = load_number_labels(size=len(data))
        # print(X.shape, y.shape)  # (2*m, 1680) (2*m, 6)

        clf = NN_Algorithm(dataX=X, labelY=y)
        return clf

    def identify_operator(self, data):
        t, _product = data.shape, 1
        for i in range(len(t)): _product *= t[i]
        data = data.reshape((1, _product))

        data = self.operator_pca.transform(data)
        lst = list(self.operator_clf.predict([data[0]])[0])
        try:
            idx = lst.index(1)
            # return list(Operator_Map.keys())[list(Operator_Map.values()).index(idx)]
        except ValueError as e:
            return 'identify_operator_failed'
        ret = 'plus'
        if idx // 2 == 2:
            ret = 'multi'
        elif idx // 2 == 1:
            ret = 'minus'
        return ret

    def identify_number(self, data):
        t, _product = data.shape, 1
        for i in range(len(t)): _product *= t[i]
        data = data.reshape((1, _product))

        data = self.num_pca.transform(data)
        lst = list(self.num_clf.predict([data[0]])[0])
        try:
            idx = lst.index(1)
            # return list(Number_Map.keys())[list(Number_Map.values()).index(idx)]
        except ValueError as e:
            return 'identify_num_failed'
        ret = 'unknown'
        temp = idx // 3
        if temp < 9: ret = str(temp + 1)  # '1' -- '9'
        return ret

    def identify_verifCodePic(self, img_path):
        img = ndimage.imread(img_path)
        # print(img.shape, img.dtype)  # (28, 90, 3)
        _img = img[:, :20, :]
        num1 = self.identify_number(data=_img)
        _img = img[:, 20:20 * 2, :]
        operator = self.identify_operator(data=_img)
        _img = img[:, 20 * 2:20 * 3, :]
        num2 = self.identify_number(data=_img)

        return num1, operator, num2


if __name__ == '__main__':
    factory = ModelFactory()
    # temp_dir = os.path.abspath('../imgs')
    # for i in range(501, 511):
    #     file_path = os.path.join(temp_dir, 'verifCodePic' + str(i) + '.jpg')
    #     factory.identify_verifCodePic(file_path)

    # missed_match_count = 0
    # for i in range(len(data)):
    #     _arr = clf.predict([X[i]])[0]
    #     if not (_arr == y[i]).all(): missed_match_count += 1
    # print(missed_match_count)
