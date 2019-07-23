# 
# 
# ctmd！先把所有的文件变成UTF-8 NO-BOM格式！！！
# 
# 
CUR_DIR = r'E:/github/kechuang/Sub-Ob-jective/'

import pynlpir

def get_list(filename):
    """
    读取文件
    """
    with open(CUR_DIR+filename, 'r', encoding='utf-8') as f:
        data_list = f.readlines()
    if(filename in ['ob.txt','sub.txt']): # 已经分类过的主观、客观文本
        data_list = [x.strip()[1:-1] for x in data_list] # 去掉两头的""
    elif(filename == 'data5.csv'): # HowNet 5类，程度副词、情感正面、情感负面、评价正面、评价负面、第一人称、标点符号
        data_list = [x.strip().split(',')[0] for x in data_list] # 只留第一列
    elif(filename == 'qinggancihui.csv'): # 大连理工 情感词汇
        data_list  = [x.strip() for x in data_list]
    return data_list

def cut(data_list):
    """
    分词
    """
    pynlpir.open()
    data_list = [(pynlpir.segment(x)) for x in data_list]
    pynlpir.close()
    return data_list

def join_cut(data_cut_list):
    """
    用空格连接
    """
    data_join_list = [' '.join([i[0] for i in x]) for x in data_cut_list]
    return data_join_list

# 打开主观和客观弹幕，并进行词性分词，再用空格连接
dm_ob = get_list('ob.txt')
dm_cut_ob = cut(dm_ob)
dm_join_ob = join_cut(dm_cut_ob)

dm_sub = get_list('sub.txt')
dm_cut_sub = cut(dm_sub)
dm_join_sub = join_cut(dm_cut_sub)

# 合并，取出分词后的不重复的文本列表
temp = dm_cut_ob + dm_cut_sub
dm_list = [j for i in temp for j in i]
dm_list = [x[0] for x in dm_list]
dm_list = list(set(dm_list))

# 打开HowNet 5类特征
data5_list = get_list('data5.csv')

# 打开大连理工情感词汇
qinggan_list = get_list('qinggancihui.csv')

# data5_list与qinggan_list取并集
l = list(set(qinggan_list).union(set(data5_list)))

# l再与dm_list取交集
l = list(set(dm_list).intersection(set(l)))

len(l) # 返回249，有足够的特征



# # tf-idf
# dm_join = dm_join_ob+dm_join_sub
# from sklearn import feature_extraction
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
# # dm_join_ob
# # corpus=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开  
# #     "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果  
# #     "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果  
# #     "我 爱 北京 天安门"]#第四类文本的切词结果  
# corpus = dm_join
# vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
# transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
# tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
# word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
# weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
# for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
#     print(u"-------这里输出第",i,u"类文本的词语tf-idf权重------")
#     for j in range(len(word)):  
#         print(word[j],weight[i][j])


