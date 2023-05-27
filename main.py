import os
import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Опции для запуска браузера в режиме headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Инициализация драйвера с помощью WebDriver Manager и опций headless
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# Переход на страницу
url = 'https://www.moex.com/ru/issue.aspx?board=TQBR&code=VSMO&utm_source=www.moex.com&utm_term=vsmpo'
driver.get(url)

# Поиск элемента на странице
driver.find_element(By.XPATH, "//div[@id='disclaimer-modal']//a[.='Согласен']").click()
element = driver.find_element(By.XPATH, "//div[@class='em_right_top']/span[@class='price']")
text_price = element.text
# Вывод текста элемента
print(text_price)

# Закрытие браузера
driver.quit()

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
text = text.replace("text_price", text_price)
send_message_to_channel(text)
