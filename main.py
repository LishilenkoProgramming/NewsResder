import cx_Oracle 
import random 
import parsing
import DB

from DemoBot import DemoBot

def start_command(message,bot):
   return ("""  Здравствуй, уважаемый пользователь!
Я могу показать Вам актуальные новости!
Вам нужно написать "Собери новости" и указать количество страниц
Написать "Покажи нвовсть"
Так же я могу удалить все новости из БД
Для этого достаточно ввести "Удали все новости"
   """,None)

def answer_command(mesage):
    return "Разработчик работает над модернизацией бота"

def show_news(mesage):
    result = []
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("Select id, link, title, text, link from News ")
    res=cur.fetchall() 
     
    for record in res:
       result.append(record[4])  
   
    con.commit()  
    cur.close()
    con.close()
    if len(result) == 0:
        return "Новостей нет"
        
    random.seed()   
    i = random.randint(0,len(result)-1) 
    return result[i]
def delete_all_news(mesage):
    con= cx_Oracle.connect('SYSTEM','12345678','localhost/xe')
    cur=con.cursor()
    cur.execute("DELETE from News")

    con.commit()  
    cur.close()
    con.close()
    return "Все новости стерты" 

def get_news(mesage):
    return "Со скольки страниц собрать новости?"

def gathering_news(mesage):
    pages = int(mesage.split(' ')[0])
    news = parsing.parsing(pages)
    DB.insert_into_db(news)
    return 'Новости сохранены'

def main():
    bot = DemoBot()
    bot.register_start_handler(start_command)
    bot.register_text_handler(answer_command,regexp='test')
    bot.register_text_handler(show_news, regexp='^Покажи новость')
    bot.register_text_handler(delete_all_news, regexp='^Удали все новости')
    bot.register_text_handler(get_news, regexp='^Собери новости')
    bot.register_text_handler(gathering_news,regexp='^[0-9]+ страниц')
    bot.run()
  
if __name__ == '__main__':
    main()