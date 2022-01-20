import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import cx_Oracle


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

def get_all_links(pages):
    # PAGENATION=input('Глубина парсинга(количество страниц): ')
    PAGENATION=pages
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

def parsing(pages):
    links=get_all_links(pages)
    news=[]
    newss=[]
    for link in links:
        news.append(get_content(link))
    for i in range(len(news)):
        newss+=list(news[i])
        #print('.',end='')
    return newss

