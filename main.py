import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Токен бота и chat_id
bot_token = '7322043838:AAGWU-m7pmNV3htMIs9o7BGktVVsGz4PqQM'
chat_id = '599532873'

# Инициализация бота
bot = telebot.TeleBot(bot_token)

# URL целевой страницы с объявлениями
url = 'https://poshmark.com/'

# Прокси (HTTP/HTTPS)
proxies = {
    'https': 'http://VWdeo5:LYu3bz@186.65.121.12:8000'  # Пример прокси, который вы можете использовать
}

# Заголовки для запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'ACCEPT-ENCODING' : 'gzip, deflate, br',
    'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'REFERER' : 'https://www.google.com/'
}

def fetch_ads():
    try:
        # Получаем HTML-страницу
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Проверка на успешный запрос

        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все объявления на странице
        ads = soup.find_all('div', class_='d--fl ai--c jc--sb')  # Замените на актуальный CSS-селектор

        fresh_ads = []

        for ad in ads:
            # Парсинг ссылки на объявление (можно заменить на другой атрибут или текст)
            ad_link = ad.find('a')['href']
            fresh_ads.append(ad_link)

        # Если найдены свежие объявления, отправляем их в Telegram
        if fresh_ads:
            for ad in fresh_ads:
                bot.send_message(chat_id, f'Свежая объявление: {ad}')
        else:
            bot.send_message(chat_id, 'Нет новых объявлений.')

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

# Запуск бота
bot.polling(none_stop=True)
