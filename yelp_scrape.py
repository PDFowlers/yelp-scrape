from email.policy import default
import requests
from bs4 import BeautifulSoup
from time import sleep
import os
from pathlib import Path
import click

# this project is aimed at searching yelp for various good and services and providing a "top 5" list of
# recommendations to the user

# get_search_request will prompt the user for a search item and a location and return those as strings we can use
# to scrape the correct webpages
<<<<<<< HEAD
@click.group(chain=True)
def cli():
    pass

# def get_search_request():
#     search_item = input(f'Please input a good or service you would like recommendations for: ')
#     sleep(0.5)
#     location = input('Please input the location you would like to search, with each item separated by'
#                      ' a comma. (ex. Detroit, Michigan, 48127): ')
#     return search_item, location

# help = 'search query for Yelp.com. Ex. "chinese food"'
# help = 'location is the area you would like to search such as city or postal code'
# url_generator will take the outputs of get_search_request and use them to generate a url that can then be used
# by requests.get
@click.command()
@click.argument('search_item')
@click.argument('location')
@click.argument('file_path', type = click.Path(exists=True))
def url_generator(search_item: str, location: str) ->str:
=======
@click.group()
def cli():
    pass
    
def url_generator(search_item: str, location: str) ->str:
    '''
    generate a url and file_name for use in the local_cache_check function
    :param str search_item: specific query for yelp (ex. chinese food)
    :param str location: area in which to look for hits on yelp (ex. Detroit, MI 48127)
    '''
>>>>>>> 2f10375f3e72baedf833844e5c2958db962fdde3
    base_url = 'https://www.yelp.com/search?'
    search_item = str(search_item).replace(' ', '+')
    location = str(location).replace(' ', '+').replace(',', '%2C')
    url = base_url + 'find_desc=' + search_item + '&find_loc=' + location
    file_name = search_item + location + '.html'
<<<<<<< HEAD
    return local_cache_check(url, file_name, file_path)

# local_cache_check will take the search request url and check a local directory for a file of the same name
# if the file is found then it will use that file instead of scraping the internet
@click.command()
# @click.argument('file_path', type = click.Path(exists=True))
def local_cache_check(url: str, file_name: str, file_path: Path) -> BeautifulSoup:
    # url_hash = hash(url)
    # path = input('Please enter complete filepath to search: ')
    print('check')
    file_list = os.listdir(f'{file_path}')
    file_path = os.path.join(file_path, file_name)
    if file_name in file_list:
        print('Retrieving the file from the directory')
        with open(file_path, 'r') as file:
=======
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
    file_list = os.listdir(f'{cache}')
    cache = os.path.join(cache, file_name)
    if file_name in file_list:
        print('Retrieving the file from the directory')
        with open(cache, 'r') as file:
>>>>>>> 2f10375f3e72baedf833844e5c2958db962fdde3
            yelp_soup = file.read()
    else:
        print('Writing new file in the directory')
        yelp_page = requests.get(url)
        yelp_soup = BeautifulSoup(yelp_page.content, 'html.parser')
<<<<<<< HEAD
        with open(file_path, 'w') as file:
            file.write(yelp_soup)
    return yelp_soup


cli.add_command(url_generator)
cli.add_command(local_cache_check)

if __name__ == "__main__":
    cli()

=======
        with open(cache, 'w') as file:
            file.write(yelp_soup)
    return yelp_soup

def collect_webpages(soup: BeautifulSoup) -> list:
    '''
    scan through the search page and collect links to the top recommendations so the relevant info can be extracted
    :param BeautifulSoup soup: The BeautifulSoup html link to the search page resulting from the query in url_generator()
    '''
    for a in soup.find_all('a'):
        print(a['href'])



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
    yelp_soup: BeautifulSoup | str = local_cache_check(url, file_name, cache)
    yelp_soup: BeautifulSoup = BeautifulSoup(yelp_soup, 'html.parser')
    pages: list = collect_webpages(yelp_soup)

cli.add_command(yelp_scrape)

if __name__ == "__main__":
    cli()

>>>>>>> 2f10375f3e72baedf833844e5c2958db962fdde3

