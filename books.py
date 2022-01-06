#! /usr/bin/python3
import platform
import time
import datetime
import requests
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent


atb_url = "https://zakaz.atbmarket.com/catalog/1016/411/"
auchan_urls = "https://auchan.ua/ua/catalogsearch/result/?q=python"

def telegram_api(telegram_message):
    token = "XXX"
    chat_id = "-XXX"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&parse_mode=HTML" + "&disable_web_page_preview=true" + "&text=" + telegram_message
    try:
        results = requests.get(url_req)
        print(results.json())
    except:
        print("can't run requests post query")
        pass
    return print("grab done")

def startbrowser():
    if "Linux" in platform.system():
        path = "geckodriver"
    else:
        path = "geko/geckodriver.exe"
    headless = True
    options = webdriver.FirefoxOptions()
    service = Service(executable_path=path)
    options.headless = True
    if headless:
        options.add_argument('-headless')
    options.add_argument("-disable-dev-shm-usage")
    options.add_argument("-no-sandbox")
    options.add_argument('-disable-gpu')
    useragent = UserAgent().firefox
    print(useragent)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent)
    driver = webdriver.Firefox(firefox_profile=profile,service=service, keep_alive=False, options=options)
    driver.implicitly_wait(30)
    return driver



def auchan_pythonbooks_grabber(url):
    driver = startbrowser()
    try:
        driver.get(url)
        time.sleep(3)
    except:
        print("can't run webdriver auchan")
        if driver:
            driver.quit()
        pass
    source = driver.page_source
    driver.quit()
    auchan_page = Soup(source, features='html.parser')
    #print(auchan_page)
    auchan_items = auchan_page.select(".Search_results_grid__G4xpv .item_root__2UY0W .item_view__header__3FYg0")
    auchan_books = ""
    #print(len(auchan_items))

    for each in range(len(auchan_items)):
        try:
            title= auchan_items[each].a["href"]
            title_text = auchan_items[each].a.text
            price=auchan_items[each].select(".item_price__sEYUp span")
            price2= price[0].text
            price_text_str = f'<a href="https://auchan.ua{title}"><i>{each + 1}){title_text}:{price2} грн.</i></a>\n'
            auchan_books = auchan_books + price_text_str
        except:
            pass
    if len(auchan_books) == 0:
        print("не найдено не одной книги")
    print(auchan_books)
    return auchan_books

def atb_grabber(url):
    driver = startbrowser()
    try:
          driver.get(url)
          time.sleep(3)
    except:
          print("can't run webdriver atb")
          if driver:
              driver.quit()
          pass
    source = driver.page_source
    driver.quit()
    page = Soup(source, features='html.parser')
    articles = page.select("article")
    products = len(articles)
    books_str= ""
    now = datetime.datetime.now().replace(microsecond=0)+datetime.timedelta(hours=2)
    for _ in range(products):
        try:
            title = articles[_].select(".catalog-list .catalog-item__title")
            title_text = title[0].text.strip()
            product_link = title[0].a["href"]
            price = articles[_].select(".catalog-list .catalog-item__bottom .product-price__top")
            price_text = price[0].attrs["value"].strip()
            price_text_str = f'<a href="https://zakaz.atbmarket.com{product_link}"><i>{_+1}){title_text}:{price_text} грн.</i></a>\n'
            books_str=books_str + f'{price_text_str}'
        except:
            pass
        if _ == products:
            break
    atb_str = f"<pre>Книги АТБ від: {now}</pre>\n{books_str}"
    print(atb_str)
    return  atb_str

#run atb scrapper:
atb_message = atb_grabber(atb_url)
time.sleep(5)
#run auchan scrapper:
auchan_message = auchan_pythonbooks_grabber(auchan_urls)
time.sleep(2)
#configure the right string for our Telegram message:
telegram_msg = atb_message + "<pre>Книги Ашан(Python):</pre>" + auchan_message

print(telegram_msg)
#run telegram_api function with configured telegram message
telegram_api(telegram_msg)
