# -*- coding:utf-8 -*-

CUR_DIR = r'E:/github/kechuang/Sub-Ob-jective/'

# 程度副词、情感正面、情感负面、评价正面、评价负面、第一人称、标点符号
with open(CUR_DIR+'data.csv', 'r') as f:
    data_list = f.readlines()
data_list = [x.strip().split(',')[0] for x in data_list]


# # Bayes
# from sklearn import datasets
# iris = datasets.load_iris()
# iris.data[:5]
# # array([[ 5.1,  3.5,  1.4,  0.2],
# #       [ 4.9,  3. ,  1.4,  0.2],
# #       [ 4.7,  3.2,  1.3,  0.2],
# #       [ 4.6,  3.1,  1.5,  0.2],
# #       [ 5. ,  3.6,  1.4,  0.2]])

# # 我们假定sepal length, sepal width, petal length, petal width 4个量独立且服从高斯分布，用贝叶斯分类器建模
# from sklearn.naive_bayes import GaussianNB
# gnb = GaussianNB()
# y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
# right_num = (iris.target == y_pred).sum()
# print("Total testing num :%d , naive bayes accuracy :%f" %(iris.data.shape[0], float(right_num)/iris.data.shape[0]))
# # Total testing num :150 , naive bayes accuracy :0.960000


