import requests
from bs4 import BeautifulSoup
from time import sleep


# this project is aimed at searching yelp for various good and services and providing a "top 5" list of
# recommendations to the user

# get_search_request will prompt the user for a search item and a location and return those as strings we can use
# to scrape the correct webpages

def get_search_request():
    search_item = input('Please input the good or service you would like recommendations for: ')
    sleep(0.5)
    location = input('\nPlease input the location you would like to search, with each item separated by'
                     ' a comma. (ex. Detroit, Michigan, 48127): ')
    return search_item, location

# url_generator will take the outputs of get_search_request and use them to generate a url that can then be used
# by requests.get
def url_generator(search_item, location):
    base_url = 'https://www.yelp.com/search?'
    search_item = search_item.replace(' ', '+')
    location = location.replace(' ', '+').replace(',', '%2C')
    url = base_url + 'find_desc=' + search_item + '&find_loc=' + location
    return url


search, loc = get_search_request()
yelp_page = requests.get(url_generator(search, loc))
yelp_soup = BeautifulSoup(yelp_page.content, 'html.parser')

test = yelp_soup.find_all('a')
links = []
for a in test:
    links.append(a["href"])

print(links)
