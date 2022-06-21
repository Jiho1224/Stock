import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import rpy2.robjects as robjects


url = "https://finance.naver.com/item/board.naver?code="
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
client = MongoClient('localhost', 27017)
db = client.stock
db.comment.drop()

search = input('찾고자하는 종목명을 입력하세요.')
con = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\collections.db")

ksq_list = pd.read_sql("SELECT * FROM itemName_KOSDAQ", con, index_col=None)
ksp_list = pd.read_sql("SELECT * FROM itemName_KOSPI", con, index_col=None)

new_list = pd.concat([ksq_list,ksp_list])

code = -1
for l in range(len(new_list)):
    if new_list.iloc[l]['name'] == search:
        code = new_list.iloc[l]['code'][1:]

if code != -1:
    #comment = pd.DataFrame([])
    comment = []
    url += code

    for i in range(50):

        try:
            temp_url = url+"&page="+str(i+1)

            html = requests.get(temp_url,headers=headers)

            bs_obj = BeautifulSoup(html.text, "html.parser")
            table = bs_obj.find('table', {'class': 'type2'})
            tt = table.select('tbody > tr')

            for i in range(2, len(tt)):

                if len(tt[i].select('td > span')) > 0:

                    temp = {}
                    date = tt[i].select('td > span')[0].text
                    title = tt[i].select('td.title > a')[0]['title']
                    pos = tt[i].select('td > strong')[0].text
                    neg = tt[i].select('td > strong')[1].text

                    temp['date'] = date
                    temp['comment'] = title
                    temp['positive'] = pos
                    temp['negative'] = neg
                    db.comment.insert_one(temp)
                    comment.append(temp)
        # table = pd.DataFrame({'날짜': [date],
        #                       '제목': [title],
        #                       '공감': [pos],
        #                       '비공감': [neg]
        #                       })
        except:
            break





