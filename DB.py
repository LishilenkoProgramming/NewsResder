import requests
from bs4 import BeautifulSoup, BeautifulStoneSoup
import cx_Oracle
import parsing 

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
    cur.executemany("""INSERT INTO news (title, news_time, text, link)
    values (:1, :2, :3, :4)""", rows)
     
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
    cur.execute("update news set title=:1, news_time=:2, text=:3, link=:4 where id=:5",
    arg_sql)
     
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


