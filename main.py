import datetime as dt
import requests
from fake_useragent import UserAgent
import bs4

KEYWORDS = ['Python', 'Go', 'Аналитика']  # Добавить в список слова для поиска
URl = 'https://habr.com'
headers = {
	'User-Agent': UserAgent().chrome,
	'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

resp = requests.get(URl, headers=headers)
soup = bs4.BeautifulSoup(resp.text, features='html.parser')
articles_list = soup.find_all('article')
for article in articles_list:
	# Теги статьи
	hubs = [hub.text.replace(' *', '').strip() for hub in article.find_all(class_='tm-article-snippet__hubs-item')]
	article_header = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2')  # Заголовки статьи
	# Получение ссылки на статью
	article_url = URl + article_header.find(class_='tm-article-snippet__title-link').attrs['href']
	resp_body = requests.get(article_url, headers=headers)  # Запрос на всю статью
	soup_body = bs4.BeautifulSoup(resp_body.text, features='html.parser')  # Создаем объект bs4
	article_body = soup_body.find(xmlns="http://www.w3.org/1999/xhtml")  # Находим текст статьи
	datetime_obj = article.find(class_="tm-article-snippet__datetime-published").find('time').attrs['datetime']
	article_date = dt.datetime.strptime(datetime_obj, '%Y-%m-%dT%H:%M:%S.%fZ')  # Перевод в формат дату и время
	for pattern in KEYWORDS:  # Итерируемся по списку слов для поиска
		# Если искомое слово в тексте статьи или в тегах или в заголовках
		if article_body.text.find(pattern) != -1 or pattern in hubs or pattern in article_header.text.split():
			print(f'{article_date.date()} - {article_header.text} - {article_url}')
