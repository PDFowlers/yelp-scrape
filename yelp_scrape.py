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
@click.group()
def cli():
    pass
    
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
    file_list = os.listdir(f'{cache}')
    cache = os.path.join(cache, file_name)
    if file_name in file_list:
        print('Retrieving the file from the directory')
        with open(cache, 'r') as file:
            yelp_soup = file.read()
    else:
        print('Writing new file in the directory')
        yelp_page = requests.get(url)
        yelp_soup = BeautifulSoup(yelp_page.content, 'html.parser')
        with open(cache, 'w') as file:
            file.write(yelp_soup)
    return yelp_soup




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
    yelp_soup = local_cache_check(url, file_name, cache)
    yelp_soup = BeautifulSoup(yelp_soup, 'html.parser')
    print(yelp_soup)

cli.add_command(yelp_scrape)

if __name__ == "__main__":
    cli()


