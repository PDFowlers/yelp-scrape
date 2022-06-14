from email.policy import default
import requests
from bs4 import BeautifulSoup
from time import sleep
import os
from pathlib import Path
import click
import re
from dataclasses import dataclass, asdict

# this project is aimed at searching yelp for various good and services and providing a "top 5" list of
# recommendations to the user

# get_search_request will prompt the user for a search item and a location and return those as strings we can use
# to scrape the correct webpages
@click.group()
def cli():
    pass

@dataclass (frozen=True)
class YelpInfo:
    '''class to store detailed yelp result info'''
    title: str      # name of business
    rating: str     # business rating based on a 5 star scale
    website: str   # specific business webpage
    phone_number: str      # business phone number. stored as (123) 456-7890
    address: str   # address for the business

def url_generator(search_item: str, location: str) ->str:
    '''
    generate a url and file_name for use in the local_cache_check function
    :param str search_item: specific query for yelp (ex. chinese food)
    :param str location: area in which to look for hits on yelp (ex. Detroit, MI 48127)
    '''
    base_url = 'https://www.yelp.com/search?'
    search_item = str(search_item).replace(' ', '+')
    location = str(location).replace(' ', '+').replace(',', '%2C')
    url = base_url + 'find_desc=' + search_item + '&find_loc=' + location
    file_name = search_item + location + '.html'
    return url, file_name

# local_cache_check will take the search request url and check a local directory for a file of the same name
# if the file is found then it will use that file instead of scraping the internet

def local_cache_check(url: str, file_name: str, cache: Path) -> BeautifulSoup:
    '''
    check a local cache of webpages and store a new one if the filename is not found
    :param str url: url of the yelp page for the specified query
    :param str file_name: name of the .html file stored in the local cache
    :param Path cache: location of directory storing the local cache
    '''
    cache.mkdir(exist_ok=True, parents=True)
    file_list = os.listdir(f'{cache}')
    cache = os.path.join(cache, file_name)
    if file_name in file_list:
        print('Retrieving the file from the directory')
        with open(cache, 'r') as file:
            cached_text = file.read()
            yelp_soup = BeautifulSoup(cached_text, 'html.parser')
    else:
        print('Writing new file in the directory')
        yelp_page = requests.get(url)
        yelp_soup = BeautifulSoup(yelp_page.text, 'html.parser')
        with open(cache, 'w') as file:
            file.write(yelp_page.text)
    return yelp_soup

def collect_webpages(soup: BeautifulSoup, search_item: str) -> set:
    '''
    scan through the search page and collect links to the top recommendations so the relevant info can be extracted
    :param BeautifulSoup soup: The BeautifulSoup html link to the search page resulting from the query in url_generator()
    '''
    search_item = str(search_item).replace(' ', '+')
    biz_lst: list = []
    for a in soup.find_all('a'):
        if 'href' in a.attrs:
            if a.attrs['href'].split('?')[-1] == 'osq=' + search_item and a.attrs['href'] not in biz_lst:
                biz_lst.append(a.attrs['href'])
        if len(biz_lst) >= 5:
            break
    return biz_lst

def page_info_grab(pages: list[str]) -> list[YelpInfo]:
    '''
    iterate through the pages list and pull relevant data from the associated yelp pages to place into reccommndation info
    :param list pages: list of urls from yelp
    '''
    base_url = 'https://yelp.com'
    recommendation_info = []
    for page in pages:
        sleep(1)
        url = base_url + page
        page_req = requests.get(url)
        page_soup = BeautifulSoup(page_req.text, 'html.parser')
        title = page_soup.h1.text
        rating = 'This business has not been rated'
        website = 'This business does not have a website listed on Yelp'
        phone_number = 'This business does not have a phone number listed on Yelp'
        address = 'This business does not have an address listed on Yelp'
        for label in page_soup.find_all('div'): 
            if label.get('aria-label') is not None:
                if label['aria-label'][0].isnumeric():
                    rating = label['aria-label']
                    break
        for a in page_soup.find_all('a'):
            if a.string is not None and a.string.startswith('http'):
                website = a.string
        for p in page_soup.find_all('p', class_='css-1p9ibgf'):
            if re.search('\(\d{3}\)', p.text) is not None:
                phone_number = p.text
        if not page_soup.find_all('p', class_='css-qyp8bo')[-1].text.startswith('Verified'):
            address = page_soup.find_all('p', class_='css-qyp8bo')[-1].text
        page_attributes = YelpInfo(title, rating, website, phone_number, address)
        recommendation_info.append(page_attributes)
    return recommendation_info

def print_data(reccommendation_info: list[YelpInfo]):
    for business in reccommendation_info:
        print('---------------')
        print(business.title)
        print(business.rating)
        print(business.website)
        print(business.phone_number)
        print(business.address)
        print('---------------')
        
@click.command()
@click.option('--cache', '-c', default = Path("./WebCache/"), type = click.Path(exists=False), help = "When provided, changes the location of the cache.")
@click.argument('search_item')
@click.argument('location')
def yelp_scrape(search_item: str, location: str, cache: Path):
    '''
    yelp_scrape will run the full program. Calling all necessary sub-functions and housing our CLI inputs through Click
    :param str search_item: specific query for yelp (ex. chinese food)
    :param str location: area in which to look for hits on yelp (ex. Detroit, MI 48127)
    :param Path cache: location of directory storing the local cache
    '''
    url, file_name = url_generator(search_item, location)
    yelp_soup: BeautifulSoup = local_cache_check(url, file_name, cache)
    pages: set = collect_webpages(yelp_soup, search_item)
    for page in pages:
        print(page + '\n')
    recommendation_info = page_info_grab(pages)
    print_data(recommendation_info)

cli.add_command(yelp_scrape)

if __name__ == "__main__":
    cli()