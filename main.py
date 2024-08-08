import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot_token = '7285744313:AAF1jv3pc9w_BA-_GzX7L1X0Vq6Zndt2Kvs'
chat_id = '599532873'

# Инициализация бота
bot = telebot.TeleBot(bot_token)

# URL целевой страницы с объявлениями
url = 'https://poshmark.com/'

# Прокси (HTTP/HTTPS)
proxies = {
    'https': 'http://VWdeo5:LYu3bz@186.65.121.12:8000'
}

# Заголовки для запроса (чтобы имитировать поведение браузера)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'ACCEPT-ENCODING' : 'gzip, deflate, br',
    'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'REFERER' : 'https://www.google.com/'
}

def fetch_ads():
    try:
        # Получаем HTML-страницу через прокси
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Проверка на успешный запрос

        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все объявления на странице
        ads = soup.find_all('div', class_='d--fl ai--c jc--sb')  # Пример CSS селектора для объявлений

        # Параметры фильтрации
        yesterday = datetime.now() - timedelta(days=1)
        fresh_ads = []

        for ad in ads:
            # Пример парсинга даты публикации
            date_posted = ad.find('time')['datetime']
            ad_date = datetime.fromisoformat(date_posted[:-1])

            # Пример парсинга информации о продавце (например, количество продаж)
            seller_info = ad.find('div', class_='seller-info')  # Найдите правильный CSS-селектор
            sales_count_text = seller_info.find('span', class_='sales-count').text.strip()  # Замените на актуальный
            sales_count = int(sales_count_text.split()[0].replace(',', ''))  # Пример парсинга числа продаж

            # Логика фильтрации
            if ad_date > yesterday and sales_count < 10:  # Пример фильтрации по количеству продаж
                ad_link = ad.find('a', class_='ad-title')['href']
                fresh_ads.append(ad_link)

        # Если найдены свежие объявления, отправляем их в Telegram
        if fresh_ads:
            for ad in fresh_ads:
                bot.send_message(chat_id, f'Свежая объявление: {ad}')
        else:
            bot.send_message(chat_id, 'Нет новых объявлений за последний день.')

    except requests.exceptions.RequestException as e:
        # В случае ошибки запроса выводим сообщение
        bot.send_message(chat_id, f'Ошибка при попытке получить доступ к сайту: {e}')

# Функция для отправки кнопки пользователю
def send_reload_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reload_button = KeyboardButton("Перезагрузить бота")
    markup.add(reload_button)
    bot.send_message(chat_id, "Нажмите кнопку, чтобы обновить объявления.", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: message.text == "Перезагрузить бота")
def reload_ads(message):
    bot.send_message(chat_id, "Обновление...")
    fetch_ads()

# Отправка кнопки при запуске
send_reload_button()

# Чтобы бот продолжал работать и не закрывался (например, если хотите добавить обработчики команд)
bot.polling(none_stop=True)
