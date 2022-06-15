import requests
from bs4 import BeautifulSoup
from random import choice
import urllib.request
from pymongo import MongoClient



client = MongoClient("mongodb+srv://1234:1234@cluster0.apyxq.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
parser = db.parser

userparsers = open('userparser.txt').read().split('\n')

userparser = {'Userparser': choice(userparsers)}


# полчуение html страницы
def get_html(url, userparser=None, proxies=None):
    r = requests.get(url, headers=userparser, proxies=None)
    return r.text


# Получение всех страници
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='G-adf').find_all('a')[-1].get('href')
    result = 'https://v1.ru/' + pages
    return result


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='B3f-').find_all('article', class_='M9az7')
    for c, item in enumerate(items, 1):
        # time.sleep(1)
        try:
            title = item.find('div', class_='M9az9').find('a').get('title')
            url = "https://v1.ru/" + item.find('div', class_='M9az9').find('a').get('href')
            datetimes = item.find('div', class_='M9a0n').find('time').get('datetime')
            count_view = item.find('div', class_='MJaxd').find('span').get_text()
            # проверка на наличие комментариев
            if item.find('a', class_='MJfj MJd3') != None:
                count_comment = item.find('a', class_='MJfj MJd3').find('span').get_text()
            else:
                count_comment = None


            # достаем полностью текст

            text_url = ''
            for i in BeautifulSoup(get_html(url), 'lxml').find_all('div', class_='MFawd'):
                for j in i.find_all('p'):
                    text_url += j.get_text()
            i = {
              'title': title,
               'url': url,
                'text': text_url,
               'datetime': datetimes,
                'count_comment': count_comment,
               'count_view': count_view,

            }

            n = parser.insert_one(i)
            print("Название новости:" + title)
            print("Количество просмотров:" + count_view)
            print("Количество комментариев:", count_comment)
            print("Дата публикации:" + datetimes)
            print(url)
            print("Текст записи:" + text_url)
        except Exception as e:
            # Выводит ошибку
            print(e)
            print("EXCEPT{}\n".format(c))
            continue


url = 'https://v1.ru/'
base_url = 'https://v1.ru/text/?'
page_part = 'page='

total_pages = 40

for i in range(1, int(total_pages) + 1):
    url_gen = base_url + page_part + str(i)
    html = get_html(url_gen, userparser)
    get_page_data(html)

