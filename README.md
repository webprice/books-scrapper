# Python web scrapper with Selenium, geckodriver and BeautifulSoup

This web scrapper was created for my own personal purposes. Since I'm learning Python and coding Python, I have an interest in Python-related books. 
Scrapper goes thru two popular retail shops, checks for suitable books, collect the information, transform the information to right markup and send it over the telegram bot, three times per day.

## How it works?

Script has 4 major functions. 
- The main function is "startbrowser()" - which starts geckodriver with Firefox settings. Script running on VPS, server without a gpu - thats why browser instance is headless. To overcome the "robots" blocks - I'm using fake-agent module, each time startbrowser function got called - browser starts with completely new firefox "headers".
- atb_grabber() and auchan_pythonbooks_grabber() - are common BeautifulSoup functions, the main idea is to - run the headless browser, navigate thru the link, save contents with "driver.get(url)" and later parse it with bs4 tools, such as "Soup(source, features='html.parser')". Return formatted string(books names, prices and links to the items). Both functions are pretty much the same, atb_grabber() - parse all books in the specific catalog(because the catalog is small and there is no need to filter the results).  auchan_pythonbooks_grabber() - parse specific "search" link with "python" keyword(because there is no filter setting on the website and the amount of books are overhelming), the possible reproduction: parse all books from the website, declate variable with list of keywords and compare each keyword for the presence in the title of the book, but it's ram,processor and time consuming, it's easier to paste the right parameter to the "search" link.
- telegram_api() fucntion - common telegram bot function which send the get request to a specific assembled link. 

## How to use
Run it with your local enviroment or pycharm with or without a telegram bot.

Run it on the Linux server as a scheduled cron job.

You can delete the telegram function from the code and script will give you "print()" results.
