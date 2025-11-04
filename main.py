import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'

response = requests.get(URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('article', class_='tm-articles-list__item')
print(f'Всего статей: {len(articles)}\n')

matching_articles = []

for article in articles:
    link_tag = article.find('a', class_='tm-title__link')
    if not link_tag:
        continue
    link = 'https://habr.com' + link_tag['href']

    try:
        art_resp = requests.get(link)
        art_resp.raise_for_status()
    except Exception as e:
        continue

    art_soup = BeautifulSoup(art_resp.text, 'html.parser')

    # Заголовок
    title_tag = art_soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else ''

    # Дата
    time_tag = art_soup.find('time')
    date = time_tag.get('datetime', '').split('T')[0] if time_tag else ''

    # Текст статьи
    content_div = art_soup.find('div', id='post-content-body')
    if not content_div:
        content_div = art_soup.find('div', class_='tm-article-body')
    text = content_div.get_text(strip=True) if content_div else ''

    # Теги (хабы) — только для поиска, не выводим
    hubs = []
    hub_links = art_soup.find_all('a', class_='tm-publication-hub__link')
    for hub in hub_links:
        hubs.append(hub.get_text(strip=True))
    hubs_text = ' '.join(hubs)

    # Поиск ключевых слов (в нижнем регистре)
    search_text = f"{title} {text} {hubs_text}".lower()
    found = any(word.lower() in search_text for word in KEYWORDS)

    if found:
        result = f"Дата: {date}\nЗаголовок: {title}\nСсылка: {link}\n"
        matching_articles.append(result)

# Вывод результата
print(f'Подходящих статей: {len(matching_articles)}\n')

with open('result.txt', 'w', encoding='utf-8') as f:
    for article in matching_articles:
        print(article)
        f.write(article + '\n')

print("Результат сохранён в файл result.txt")