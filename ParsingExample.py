import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import cx_Oracle
import numpy as np

HOST = 'https://www.kommersant.ru/'
URL = 'https://www.kommersant.ru/theme/3378'



def get_html (URL, params=''):
    r= requests.get(URL,params=params)
    return r

def get_links(html):
    soup= BeautifulSoup(html.text,'html.parser')
    items= soup.find_all('article', class_='uho rubric_lenta__item')
    
    links= []
   
    for item in items:
        links.append(
            (
                HOST + item.find('a',class_='uho__link uho__link--overlay').get('href')              

            )
        )
    return links

def get_all_links():
    PAGENATION=input('Глубина парсинга(количество страниц): ')
    PAGENATION=int(PAGENATION.strip())
    html=get_html(URL)
    

    if html.status_code== 200:
        html=get_html(URL)
        links=get_links(html)
        for page in range(1,PAGENATION):
            html= get_html(URL,params={'page':page})
            links.extend(get_links(html))

    else:
        print ('Error')
    return(links)

def get_content(URL):
    html= requests.get(URL)
    soup= BeautifulSoup(html.text,'html.parser')
    items= soup.find_all('div', class_='main grid')
    news= []  

    for item in items: 
        row =  item.find_all('p',class_='doc__text')      
        news_desc = '';
        for x in row:
          news_desc += x.get_text(strip=True).replace('\xa0',' ')
        news.append(
            (                              
                item.find('h1',class_='doc_header__name js-search-mark').get_text(strip=True),
                item.find('time',class_='doc_header__publish_time').get_text(strip=True),
                news_desc,
                URL  
            )        
        )
    return news

def parsing(url):
    links=get_all_links()
    news=[]
    for link in links:
        news.append(get_content(link))
    for i in range(len(news)):
        news+=list(news[i])
        #print('.',end='')
    return news

def create_table():
       
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("""CREATE table news ("ID" NUMBER GENERATED ALWAYS AS IDENTITY 
    MINVALUE 1 MAXVALUE  9999999999999999999999999999
    INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER 
    NOCYCLE  NOKEEP  NOSCALE , 
	"TITLE" VARCHAR2(1000 BYTE), 
	"NEWS_TIME" VARCHAR2(1000 BYTE), 
	"TEXT" CLOB, 
	"LINK" VARCHAR2(1000 BYTE))""")
         
    con.commit()  
    cur.close()
    con.close()

def insert_into_db(rows):
    if rows==None:
        return
    
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.executemany("INSERT INTO news (title, news_time, text, link) values (:1, :2, :3, :4)", rows)
     
    con.commit()  
    cur.close()
    con.close()

def delete_from_db(id):
    if type(id) != int:
        return
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("delete from news where id=:1",[id] )

    con.commit()  
    cur.close()
    con.close()

def update_db(row, id):
    if type(row)!= list and type(row)!=tuple:
        return
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    arg_sql = list(row)
    arg_sql.append(id)
    cur.execute("update news set title=:1, news_time=:2, text=:3, link=:4 where id=:5", arg_sql)
     
    con.commit()  
    cur.close()
    con.close()

def read_db():
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("Select id, link, title from News ")
    res=cur.fetchall() 
     
    for record in res:
        
        print(record)
   
    con.commit()  
    cur.close()
    con.close()

# news=parsing(URL)- парсит статьи по заданному количеству страниц
# create_table() - создание таблицы для выгрузки данных
# insert_into_db(news) - функция выгрузки данных 
# read_db() - чтение таблицы
# update_db((1,2,3,4),102) - пример обновления данных в таблице
#delete_from_db(100) - пример удаления данных из таблицы через ID

