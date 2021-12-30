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


# html=get_html(URL)
# #print(html.text)
# a=get_links(html)
# print(a)


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
        news.append(
            (  
                            
                item.find('h1',class_='doc_header__name js-search-mark').get_text(strip=True),
                item.find('time',class_='doc_header__publish_time').get_text(strip=True),
                item.find('p',class_='doc__text').get_text(strip=True), 
                URL  
        )        
        )
    return news



def parsing(url):
    links=get_all_links()
    news=[]
    for link in links:
        news.append(get_content(link))
    return news

news=parsing(URL)
nnews=[]

for i in range(len(news)):
    for j in range(len(news)):
        news[j].insert(0,j+1)
    nnews+=list(news[i])
print(nnews)


# news=[]
# for i in range(len(nnews)):
#     news+=list(nnews[i])




# print(news)
# final_news= [item for sublist in news for item in sublist]
# for elem in final_news:
#     el = elem.text
#     news.append(el)
#print (news)

def create_table():
       
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("CREATE table news (id number primary key, title varchar2(1000), news_time varchar2(1000), text varchar2(3999), link varchar2(1000))")
         
    con.commit()  
    cur.close()
    con.close()

# create_table()

def insert_into_db(rows):
    if rows==None:
        return
    
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.executemany("INSERT INTO news (id, title, news_time, text, link) values (:1, :2, :3, :4, :5)", rows)
     
    con.commit()  
    cur.close()
    con.close()

insert_into_db(nnews)

def delete_from_db(id):
    if type(id) != int:
        return
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    #sql = "delete from news where id=" + str(id)
    #print(sql)
    cur.execute("delete from news where id=:1",[id] )
    #cur.execute(sql)
     
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
    cur.execute("update news set title=:1, link=:2 where id=:3", arg_sql)
     
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






# insert_into_db(a)



#title = input('ВВедите заголовок: ')
#link = input('ВВедите ссылку: ')

#update_db([title,link],242)
#id_remove = int(input('Введите ID, удаляемой записи: '))
#delete_from_db(id_remove)




####
# 1. insert_into_db
# 2. x = read_from_db //select ... from
# 3. найти в списке x один из id
# 4. update_db(row,id)
# 5. y = read_from_db()
# 6. print(y)
# 7. delete_from_db(id)        
# 8. z = read_from_db()
# 9. print(z) 

#  def parser():
#      PAGENATION=input('Глубина парсинга(количество страниц): ')
#      PAGENATION=int(PAGENATION.strip())

#      html=get_html(URL)

#      if html.status_code== 200:
#          news=[]
#          for page in range(1,PAGENATION):
#              html= get_html(URL,params={})


#      else:
#          print ('Error')

#  parser()




