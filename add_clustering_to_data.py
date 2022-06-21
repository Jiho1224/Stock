import pandas as pd
import sqlite3

con = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\news\correlation_code.db")
con2 = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\stocks.db")

cluster_id = pd.read_sql("SELECT * FROM clustering_kmeans", con, index_col=None)
print("cluster id 호출 완료")

cluster_list = []

# 군집화 각 list
cluster0 = pd.read_sql("SELECT code FROM clustering_kmeans WHERE cluster=0",con,index_col=None)['code'].tolist()
cluster1 = pd.read_sql("SELECT code FROM clustering_kmeans WHERE cluster=1",con,index_col=None)['code'].tolist()
cluster2 = pd.read_sql("SELECT code FROM clustering_kmeans WHERE cluster=2",con,index_col=None)['code'].tolist()
cluster3 = pd.read_sql("SELECT code FROM clustering_kmeans WHERE cluster=3",con,index_col=None)['code'].tolist()
cluster4 = pd.read_sql("SELECT code FROM clustering_kmeans WHERE cluster=4",con,index_col=None)['code'].tolist()

cur = con2.cursor()

for code in cluster0:
    sql1 = "UPDATE Table_KOSDAQ SET cluster = 0 WHERE code='"+str(code)+"'"
    sql2 = "UPDATE Table_KOSPI SET cluster = 0 WHERE code='"+str(code)+"'"

    cur.execute(sql1)
    cur.execute(sql2)
print("cluster0 완료")

for code in cluster1:
    sql1 = "UPDATE Table_KOSDAQ SET cluster = 1 WHERE code='"+str(code)+"'"
    sql2 = "UPDATE Table_KOSPI SET cluster = 1 WHERE code='"+str(code)+"'"

    cur.execute(sql1)
    cur.execute(sql2)
print("cluster1 완료")

for code in cluster2:
    sql1 = "UPDATE Table_KOSDAQ SET cluster = 2 WHERE code='"+str(code)+"'"
    sql2 = "UPDATE Table_KOSPI SET cluster = 2 WHERE code='"+str(code)+"'"

    cur.execute(sql1)
    cur.execute(sql2)
print("cluster2 완료")
for code in cluster3:
    sql1 = "UPDATE Table_KOSDAQ SET cluster = 3 WHERE code='"+str(code)+"'"
    sql2 = "UPDATE Table_KOSPI SET cluster = 3 WHERE code='"+str(code)+"'"

    cur.execute(sql1)
    cur.execute(sql2)
print("cluster3 완료")
for code in cluster4:
    sql1 = "UPDATE Table_KOSDAQ SET cluster = 4 WHERE code='"+str(code)+"'"
    sql2 = "UPDATE Table_KOSPI SET cluster = 4 WHERE code='"+str(code)+"'"

    cur.execute(sql1)
    cur.execute(sql2)
print("cluster4 완료")