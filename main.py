# -*- coding: utf-8 -*-
import os

import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_price():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver = webdriver.Chrome("/driver/chromedriver_linux64/chromedriver",options=chrome_options)
    url = 'https://www.moex.com/ru/issue.aspx?board=TQBR&code=VSMO&utm_source=www.moex.com&utm_term=vsmpo'
    driver.get(url)

    # Поиск элемента на странице
    driver.find_element(By.XPATH, "//div[@id='disclaimer-modal']//a[.='Согласен']").click()
    element = driver.find_element(By.XPATH, "//div[@class='em_right_top']/span[@class='price']")
    text_price = element.text
    # Вывод текста элемента
    # print(text_price)

    # Закрытие браузера
    driver.quit()
    return text_price


def send_price_to_chat(get_price_text):
    # Вставьте токен вашего бота Telegram
    bot_token = os.environ['BOT_TOKEN']
    supergroup_username = '@+RKBDwebcUqxjMDZi'
    # Вставьте ID группы, в которую вы хотите отправить сообщение +RKBDwebcUqxjMDZi
    channel_id = -1001960945097

    # Создаем экземпляр бота
    bot = telebot.TeleBot(bot_token)

    # Отправляем сообщение в канал
    def send_message_to_channel(message):
        bot.send_message(channel_id, message, parse_mode='MarkdownV2')

    # Пример использования
    text = "\n\n📈 Стоимость 1 акции ВСМПО\\-Ависма \(VSMO\) на московской бирже составляет *text_price*\n\\#мосбиржа \\#vsmpo"
    text = text.replace("text_price", get_price_text)
    send_message_to_channel(text)


# schedule.every().monday.to.friday.at('10:00').do(send_price_to_chat(get_price()))
# while True:
#     schedule.run_pending()

import datetime
import schedule
import time
import pytz


def run_scheduled_method():
    # Установка временной зоны
    moscow_timezone = pytz.timezone('Europe/Moscow')

    # Задание расписания выполнения метода по будням в 10:00
    # schedule.every().day.at('09:59').do(print("jshdfkjhl"))

    while True:
        # Получение текущего времени в указанной временной зоне
        current_time = datetime.datetime.now(moscow_timezone)

        # Получение текущего дня недели
        current_day = current_time.weekday()
        print(current_time)
        # Проверка расписания и выполнение заданных методов только по будням
        # if current_day >= 0 and current_day <= 4 and current_time.hour == 9 and current_time.minute == 56 and current_time.second == 00:
        if current_time.hour == 14 and current_time.minute == 44 and current_time.second == 0:
            schedule.run_pending()
            send_price_to_chat(get_price())

        # Задержка в 1 секунду перед проверкой расписания снова
        time.sleep(1)


send_price_to_chat(get_price())
# Вызов функции для запуска выполнения метода по расписанию
run_scheduled_method()
