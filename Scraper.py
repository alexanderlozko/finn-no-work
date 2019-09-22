from bs4 import BeautifulSoup
import requests
import re

#page = 2
#url = 'https://www.finn.no/realestate/newbuildings/search.html?page='+page+'&sort=1'
url = 'https://www.finn.no/realestate/newbuildings/search.html?sort=1'

response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')

list_of_url = []

class Scraper:

    @staticmethod
    def scrape_url(soup):

        div_news = soup.find_all('div', {'class': ['ads__unit__content']})

        for article in div_news:

            try:
                url = article.a['href']                                                                        #url
                name = article.a.string                                                                        #name
                location = article.span.span.string                                                            #location
                company = article.find_all('span',{'class':["ads__unit__content__list truncate"]})[0].string   #company


            except AttributeError:
                location = None
                print(location)
                continue

            except TypeError:
                url = None
                print(url)
                continue
            if url == None:
                url = None
            else:
                url = 'http://finn.no' + url
                list_of_url.append(url)

            response = requests.get(url)
            soup = BeautifulSoup(response.text,'html.parser')
            result = soup.find_all('div', {'class':['contact mbl pbl']})

            person = result[0].h3.string                                                     #person
            mobile = result[0].find_all('a', {'class':['blockify pvm txtcolor']})[2].string
            mobile = re.search(r'\d{3}\s\d{2}\s\d{3}', mobile)[0]                            #mobile

            landline = result[0].find_all('a', {'class':['blockify pvm txtcolor']})[3].string
            try:
                landline = re.search(r'\d{2}\s\d{2}\s\d{2}\s\d{2}', landline)[0]             #landline
            except TypeError:
                landline = None
            print(landline)


Scraper.scrape_url(soup)


