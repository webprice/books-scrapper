# Python web scrapper with Selenium, geckodriver and BeautifulSoup

This web scrapper was created for my purposes. Since I'm learning Python and coding Python, I have an interest in Python-related books. 
Scrapper goes thru two popular retail shops, checks for suitable books, collect the information, transform the information to the right markup and send it over to the telegram bot, three times per day.

## How it works?

Script has 4 major functions. 
- The main function is "startbrowser()" - which starts geckodriver with Firefox settings. The script running on VPS, a server without a GPU - that's why the browser instance is headless. To overcome the "robots" blocks - I'm using a fake-agent module, each time startbrowser() function got called - the browser starts with completely new firefox "headers".
- atb_grabber() and auchan_pythonbooks_grabber() - are common BeautifulSoup functions, the main idea is to - run the headless browser, navigate thru the link, save contents with "driver.get(url)" and later parse it with bs4 tools, such as "Soup(source, features='html.parser')". Return formatted string(books names, prices and links to the items). Both functions are pretty much the same, atb_grabber() - parse all books in the specific catalogue (because the catalogue is small and there is no need to filter the results).  auchan_pythonbooks_grabber() - parse specific "search" link with "python" keyword(because there is no filter setting on the website and the number of books is overwhelming), the possible reproduction: parse all books from the website, declare a variable with a list of keywords and compare each keyword for the presence in the title of the book, but it's the ram, processor and time consuming, it's easier to paste the right parameter to the "search" link.
- telegram_api() function - common telegram bot function which sends the get request to a specific assembled link. 

## How to use
Run it with your local environment or pycharm with or without a telegram bot.

Run it on the Linux server as a scheduled cron job.

You can delete the telegram function from the code and the script will give you "print()" results.

## How to install
all the necessary modules are named in `requirements.txt`

don't forget to download and install geckodriver, for Windows - you should extract it inside project folder, for Linux - you can extract and install it anywhere and Add the driver to your PATH so other tools can find it:
`export PATH=$PATH:/path-to-extracted-file/`
