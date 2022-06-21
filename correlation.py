import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

con = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\collections.db")
con2 = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\newSets.db")
con3 = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\kendall.db")

ksq_list = pd.read_sql("SELECT * FROM itemName_KOSDAQ", con, index_col=None)
ksp_list = pd.read_sql("SELECT * FROM itemName_KOSPI", con, index_col=None)

for i in range(len(ksq_list)):
    name = ksq_list['name'][i]
    try:
        name = name.replace(' ', "_")
        name = name.replace('&', "_")
        name = name.replace('(', "_")
        name = name.replace(')', "_")
        name = name.replace('-', "_")
        name = name.replace('.', "_")
        name = name.replace('%', "_")
        stock_data = pd.read_sql("SELECT * FROM " + str(name), con2, index_col=None)
        print(name)
        re = stock_data[['open', 'high', 'low', 'close', 'volume', 'market_cap',
                         'foreign', 'KOSPI', 'KOSDAQ', 'NASDAQ', 'exchange_rate', 'HangSeng',
                         'base_rate', 'bond_yield', 'gold', 'copper', 'diesel'
                         ]].corr(method='kendall')

        close_re = re['close']
        close_re.to_sql(name, con3, chunksize=1000, if_exists='replace')

    except Exception as ex:
        pass

for i in range(len(ksp_list)):
    name = ksp_list['name'][i]
    try:
        name = name.replace(' ', "_")
        name = name.replace('&', "_")
        name = name.replace('(', "_")
        name = name.replace(')', "_")
        name = name.replace('-', "_")
        name = name.replace('.', "_")
        name = name.replace('%', "_")
        stock_data = pd.read_sql("SELECT * FROM " + str(name), con2, index_col=None)

        re = stock_data[['open', 'high', 'low', 'close', 'volume', 'market_cap',
                         'foreign', 'KOSPI', 'KOSDAQ', 'NASDAQ', 'exchange_rate', 'HangSeng',
                         'base_rate', 'bond_yield', 'gold', 'copper', 'diesel']].corr(method='kendall')
        # pearson
        # spearman
        # kendall
        print(name)
        close_re = re['close']
        close_re.to_sql(name, con3, chunksize=1000, if_exists='replace')

    except Exception as ex:
        pass

# re = stock_data.corr(method='pearson')
#
# re.to_csv(r'C:\Users\user\Desktop\stock\correlation\SK_상관계수.csv',index=False)
# print(re['close'])
# sns.heatmap(re,cmap='viridis')
# plt.show()


