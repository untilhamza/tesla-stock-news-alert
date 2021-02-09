import requests
import smtplib
import os
from email.message import EmailMessage

sender = 'hamzamycode@gmail.com'
receiver = 'sanshinehamza@gmail.com'
password = os.environ['email_password']
server = 'smtp.gmail.com'
stock_dates_list = None
email_subject = None




STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = 'PI key: KQ3DZMO4I07GOE65'
NEWS_API = '8a465ac5fcce4c118909baab9e40be4a'

stock_parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY,
}

def send_news(message):
    global sender, receiver, server
    with smtplib.SMTP(server) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(message)


def check_stock():
    global date_yesterday, stock_dates_list, email_subject
    response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
    stock_data = response.json()['Time Series (Daily)']  # ['2021-01-29']
    stock_dates = list(response.json()['Time Series (Daily)'])  # the list casting gets a  list of the keys of the
    stock_dates_list = stock_dates
    date_yesterday = stock_dates[0]
    yesterday_stocks = stock_data[stock_dates[0]]['4. close']
    day_before_yesterday_stocks = stock_data[stock_dates[1]]['4. close']
    diff = float(yesterday_stocks) - float(day_before_yesterday_stocks)
    percent = round((diff / float(yesterday_stocks)) * 100, 1)
    if diff > 0:
        email_subject = f'TSLA: 🔺{percent}%'

    else:
        email_subject = f'TSLA: 🔻{percent}%'
    if abs(percent) > 5:
        return True


stock_news_parameters = {
    'q': COMPANY_NAME,
    'apiKey': NEWS_API,
    'language': 'en',
    'qInTitle': COMPANY_NAME,
    'from': stock_dates_list[3],
}


def get_news():
    global email_subject, stock_news_parameters, stock_dates_list
    stock_news_parameters['from'] = stock_dates_list[0]
    stock_news_parameters['to'] = stock_dates_list[2]
    response = requests.get(url=NEWS_ENDPOINT, params=stock_news_parameters)
    news = []
    for index in range(3):
        data = response.json()['articles'][index]
        source = data['source']['name'].strip()
        title = data['title']
        description = data['description']
        link = data['url']
        sep = '\n'
        article = source + sep + title + sep + description + sep + link
        news.append(article)

    message_content = f'''
    Dear Hamza,
    {news[0]}
    {news[1]}
    {news[2]}
    '''
    message = EmailMessage()
    message.set_content(message_content)
    message['Subject'] = f'{email_subject}  news'
    message['from'] = sender
    message['to'] = receiver
    return message


if check_stock():
    send_news(get_news())

