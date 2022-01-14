
import csv
# access test data
csvfile = open('test_revised.csv', newline = '')
test = list(csv.reader(csvfile))
del test[0]
for i in test: del i[0]
for i in range(len(test)):
    for j in range(len(test[i])):
        test[i][j]=float(test[i][j])

# access train data
trainfile = open('train_revised.csv',newline = '')
train = list(csv.reader(trainfile))
del train[0]
for i in train: del i[0]
for i in range(len(train)):
    for j in range(len(train[i])):
        train[i][j]=float(train[i][j])

# access train_label
labelfile = open('train_data_label_t.csv',newline = '')
label = list(csv.reader(labelfile))
for i in range(len(label)):
    label[i] = str(*label[i])
'''
# access test_label
file = open('test_data_label_t.csv',newline = '')
test_label = list(csv.reader(file))
for i in range(len(test_label)):
    test_label[i] = str(*test_label[i])
'''

def most_label(labels):
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

def euclidean_dist(test_row, train_row):
    distance = 0.0
    for c in range(len(test_row)-1):
        distance += (test_row[c] - train_row[c]) * (test_row[c] - train_row[c])
    return distance

def get_neighbors(idx, test_row, trainset, train_label, k):
    dists = []
    outlier = []
    for i in range(len(trainset)): # i表示train data的第幾筆資料
        dist = euclidean_dist(test_row, trainset[i]) # 每筆test data跟所有的train data計算距離
        dists.append((dist, train_label[i])) # dists[][0]: 距離,  dists[][1]: label
    dists.sort(key=lambda tup: tup[0]) # 對距離進行sorting（由小到大）
    labels = []
    if dists[0][0] > 5:
        #print(dists[0][0])
        test_row.insert(0,idx) # 把index放到第一個位置
        outlier = test_row # 距離過遠的test data, 其在test data是第幾筆
    
    for j in range(k):
        labels.append(dists[j][1])
    
    return outlier, labels

def KNN(testset, trainset, train_label, k):
    predictions = []
    outliers = []
    for idx in range(len(testset)):
        print(idx)
        outlier, labels = get_neighbors(idx, testset[idx], trainset, train_label, k)
        output = most_label(labels)
        if outlier != []:
            outliers.append(outlier)  # [[row0],[row1],...]
        predictions.append(output)
    return outliers, predictions
    
outliers, classified_outcome = KNN(test, train, label, k=5)
#for i in outliers:
#    print(i)

with open('outlier.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(outliers)

with open('classified.csv', 'w', newline='') as csvfile:
    out = csv.writer(csvfile)
    out.writerows(classified_outcome)