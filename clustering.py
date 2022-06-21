import sqlite3
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import linkage, dendrogram
import seaborn as sns
from tslearn.clustering import TimeSeriesKMeans

con = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\collections.db")
con2 = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\spearman.db")

ksq_list = pd.read_sql("SELECT * FROM itemName_KOSDAQ", con, index_col=None)
ksp_list = pd.read_sql("SELECT * FROM itemName_KOSPI", con, index_col=None)

#'name','open', 'high', 'low', 'volume', 'market_cap', 'foreign', 'ndq', 's&p', 'kosdaq', 'kospi', 'base rate'

_name = []
_open = []
_high = []
_low = []
_volume =[]
_cap = []
_foreign = []
_ndq = [] # 기존
_ksq = [] # 기존
_ksp = [] # 기존
_base = []
_exchange = []
_hangseng = []
_bond_yield = []
_gold = []
_copper = []
_diesel = []


for i in range(len(ksq_list)):
    name = ksq_list['name'][i]
    name = name.replace(' ', "_")
    name = name.replace('&', "_")
    name = name.replace('(', "_")
    name = name.replace(')', "_")
    name = name.replace('-', "_")
    name = name.replace('.', "_")
    name = name.replace('%', "_")
    try:
        stock_data = pd.read_sql("SELECT * FROM " + str(name), con2, index_col=None)


        rates = stock_data['close']
        _rates = list()
        for row in rates:
            if (np.isnan(row) == True):
                row = 0
            _rates.append(row)

        _rates.insert(0,name)
        _rates.pop(4)
        # #'open', 'high', 'low', 'volume', 'market_cap',
        #                          'foreign', 'KOSPI', 'KOSDAQ', 'NASDAQ', 'exchange_rate', 'HangSeng',
        #                          'base_rate', 'bond_yield', 'gold', 'copper', 'diesel'
        _name.append(_rates[0])
        _open.append(_rates[1])
        _high.append(_rates[2])
        _low.append(_rates[3])
        _volume.append(_rates[4])
        _cap.append(_rates[5])
        _foreign.append(_rates[6])
        _ksp.append(_rates[7])
        _ksq.append(_rates[8])
        _ndq.append(_rates[9])
        _exchange.append(_rates[10])
        _hangseng.append(_rates[11])
        _base.append(_rates[12])
        _bond_yield.append(_rates[13])
        _gold.append(_rates[14])
        _diesel.append(_rates[15])

    except Exception as e:
        pass

for i in range(len(ksp_list)):
    name = ksp_list['name'][i]
    name = name.replace(' ', "_")
    name = name.replace('&', "_")
    name = name.replace('(', "_")
    name = name.replace(')', "_")
    name = name.replace('-', "_")
    name = name.replace('.', "_")
    name = name.replace('%', "_")
    try:
        stock_data = pd.read_sql("SELECT * FROM " + str(name), con2, index_col=None)


        rates = stock_data['close']
        _rates = list()
        for row in rates:
            if (np.isnan(row) == True):
                row = 0
            _rates.append(row)

        _rates.insert(0,name)
        _rates.pop(4)

        _name.append(_rates[0])
        _open.append(_rates[1])
        _high.append(_rates[2])
        _low.append(_rates[3])
        _volume.append(_rates[4])
        _cap.append(_rates[5])
        _foreign.append(_rates[6])
        _ksp.append(_rates[7])
        _ksq.append(_rates[8])
        _ndq.append(_rates[9])
        _exchange.append(_rates[10])
        _hangseng.append(_rates[11])
        _base.append(_rates[12])
        _bond_yield.append(_rates[13])
        _gold.append(_rates[14])
        _diesel.append(_rates[15])

    except Exception as e:
        pass
dataframe = pd.DataFrame({'name':_name,'open':_open,'high':_high,'low':_low,'volume':_volume,'market':_cap,
                          'foreign':_foreign,'KOSPI':_ksp,'KOSDAQ':_ksq,'NASDAQ':_ndq,'exchange_rate':_exchange,
                          'Hangseng':_hangseng,'base_rate':_base,'gold':_gold,'diesel':_diesel})

#1. 프로토타입 기반의 군집화 (k-means)
company = dataframe.groupby('name').mean()

estimator = KMeans(n_clusters = 5)
cluster_id = estimator.fit_predict(company)


df = pd.DataFrame({'name':_name,'open':_open,'high':_high,'low':_low,'volume':_volume,'market':_cap,
                          'foreign':_foreign,'KOSPI':_ksp,'KOSDAQ':_ksq,'NASDAQ':_ndq,'exchange_rate':_exchange,
                          'Hangseng':_hangseng,'base_rate':_base,'gold':_gold,'diesel':_diesel,'cluster':cluster_id})
con3 = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\KMeans.db")
df.to_sql("Kmeans", con3, chunksize=1000, if_exists='replace')

# 각 군집 개수
cs = df.groupby(['cluster'])['name'].count()
print(cs)

# cluster = AgglomerativeClustering(n_clusters=3,affinity='euclidean',linkage='ward')
# cluster.fit_predict(data)
## 피어슨

# 0     837
# 1     837
# 2    1288

## 스피어만
# 0    1289
# 1     848
# 2     825

## 켄달
# 0     501
# 1    1308
# 2    1153


# 2. 시계열 클러스터링 --> 실제로는 시간성을 가진 개체들의 데이터를 묶어주지만
# 우리의 상관계수 데이터는 다차원이므로 각 항목에 대한 수치의 흐름 (추이) 을 볼 수 있다는 점에서 시계열 클러스터링
# 을 이용하는 것도 좋은 방법이라고 생각이 든다.

model = TimeSeriesKMeans(n_clusters=5,metric="dtw",max_iter=10)
model.fit(company)

result = model.predict(company)
df2 = pd.DataFrame({'name':_name,'cluster':result})

df2.to_sql("TimeSeriesKmeans", con3, chunksize=1000, if_exists='replace')

cs = df2.groupby(['cluster'])['name'].count()

print(cs)
