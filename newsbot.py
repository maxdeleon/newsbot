import time
import schedule
import requests
import nltk
from newspaper import Article
from googlesearch import search 


def searchLinks(query):
  article_links = []
  for j in search(query, tld="com", lang='en', start=0, num=4, stop=4, pause=1): 
    article_links.append(j)

  return article_links

def processNews(links):
  news = []
  data = []
  for x in range(len(links)):
    article = Article(links[x])

    try:
      article.download()
      article.parse()
      #nltk.download('punkt')
      article.nlp()

      title = article.title
      author = article.authors
      article_date = article.publish_date
      text = article.text
      summary = article.summary

      data = [article_date, title, author, summary, links[x]]

      news.append(data)

    except:
      print('error getting article!')

  return news


def get_news_today(query):
  from datetime import date

  current_date = date.today()
  query = query + ' ' + str(current_date)
  links = searchLinks(query)
  data = processNews(links)

  message = ''
  for y in range(len(data)):
    tag = '====='+ 'Article ' + str(y+1) + '=====' + '\n'
    title = str(data[y][1]) + '\n'
    date = str(data[y][0]) + '\n'
    summary = data[y][3] + '\n'
    link = data[y][4] + '\n'
    message = message + tag + title + date + summary + link + '\n'

  #print(message)
  return message


def telegram_bot_sendtext(bot_message):
    
    bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
    bot_chatID = 'xxxxxxxxxxxxxxxxxxxxx'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def report():
    query = 'Agfax.com'
    my_message = get_news_today(query)
    telegram_bot_sendtext(my_message)






schedule.every().day.at("9:00").do(report)
while True:
    schedule.run_pending()
    time.sleep(1)'''
