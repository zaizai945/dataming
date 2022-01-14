import numpy as np
from csv import reader

# 讀取未知類的資料
file = open('outlier.csv',newline = '')
group = list(reader(file))
#del group[0]
outlier_idx = []
for i in group:                  
    outlier_idx.append(int(i[0]))     # 把outlier在test data的index裝到一個list
    del i[0]
for i in range(len(group)):
    for j in range(len(group[i])):
        group[i][j]=float(group[i][j])

# 讀取test data label
test = open('test_data_label_t.csv',newline = '')
test_label = list(reader(test))
for i in range(len(test_label)):
    test_label[i] = str(*test_label[i])

# KNN分類後的test data label
out = open('classified.csv',newline = '')
global classified
classified = list(reader(out))
for i in range(len(classified)):
    classified[i] = str(*classified[i])

# 將每一筆outlier根據它在test data的index，對應其label
element_label = []
for i in outlier_idx:
    element_label.append(test_label[i])   # 每一筆outlier對應到的label

# 計算每個cluster最多的label是哪一種
def mostLabel(labels):
    tmplist = []
    for i in range(len(labels)):
        if labels[i] not in tmplist:
            tmplist.append(labels[i])
    maxtimes = 0
    mostlabel = -1
    for i in range(len(tmplist)):
        times = labels.count(tmplist[i])
        if maxtimes == 0:
            maxtimes = times
            mostlabel = tmplist[i]
        elif times > maxtimes:
            maxtimes = times
            mostlabel = tmplist[i]
        elif times == maxtimes:
            mostlabel = tmplist[i]
    return mostlabel

# 每個元素與k點的距離
def euclidean_dist(row, k_row):
    distance = 0.0
    for c in range(len(row)):
        distance += (row[c] - k_row[c]) * (row[c] - k_row[c])
    return distance

# 對每個元素進行分群
def cluster(outlier_idx, element_label, k_group, group, k):
    team = []
    cluster_labels = []
    cluster_idx = []
    # create empty cluster   [[[1,2,3],[2,3,1],...],[],[],...]
    for i in range(k):
        team.append([])
        cluster_labels.append([])
        cluster_idx.append([])
    tmp = float('inf')
    for i in range(len(group)):
        for j in range(len(k_group)):
            dist = euclidean_dist(group[i], k_group[j])
            if dist < tmp:
                tmp = dist
                flag = j       # 記下是第幾個cluster
        team[flag].append([*group[i]])
        cluster_labels[flag].append(element_label[i])  # 每個cluster中每個元素對應的label   [ [0,3,...], [2,4,5,...] , [6,10,1,....], ... ]
        cluster_idx[flag].append(outlier_idx[i])       # 每個cluster中每個元素在test data對應的index
        tmp = float('inf')
    return cluster_idx, cluster_labels, team

# 對分群完的元素找出新的群集中心
def find_centroid(team, k_group):
    centroid = []
    for idx, nodes in enumerate(team):
        sum = np.zeros(len(k_group[0]))    # 宣告為全為0的陣列
        if nodes == []:
            centroid.append(k_group[idx])
        else:
            for node in nodes:
                sum += node
            centroid.append( np.true_divide(sum,len(nodes)) )
            #print(centroid)
    return centroid

def kmeans(classified, outlier_idx, element_label, k_group, group, k):
    cluster_idx, cluster_labels, team = cluster(outlier_idx, element_label, k_group, group, k)
    k_coordinate = find_centroid(team, k_group)
    res = np.array_equal(k_coordinate, k_group) # 判斷兩陣列所有值是否相等
    print(res)
    if res:
        for i in range(k):
            #print(cluster_labels[i])
            cluster_labels[i] = mostLabel(cluster_labels[i]) # 計算每個cluster最多的label: [a, c, b, ...]
            for j in cluster_idx[i]:                         # 按照每個cluster中各個元素的index，去更改classified中的未知類資料
                classified[j] = cluster_labels[i]

    else: kmeans(classified, outlier_idx, element_label, k_coordinate, group, k)

############---------------------main----------------------##############

k = 22
k_group = np.random.rand(k, len(group[0]))
# idx = np.random.randint(len(group[0]), size=k)
kmeans(classified, outlier_idx, element_label, k_group, group, k)

# 計算準確率
count = 0
for i in range(len(test_label)):

    if test_label[i] == classified[i]:
        count += 1
print(count / len(test_label))
