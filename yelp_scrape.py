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
def url_generator(search_item: str, location: str) ->str:
    base_url = 'https://www.yelp.com/search?'
    search_item = str(search_item).replace(' ', '+')
    location = str(location).replace(' ', '+').replace(',', '%2C')
    url = base_url + 'find_desc=' + search_item + '&find_loc=' + location
    file_name = search_item + location + '.html'
    return url, file_name

# local_cache_check will take the search request url and check a local directory for a file of the same name
# if the file is found then it will use that file instead of scraping the internet
@click.command()
@click.argument('file_name', type = click.Path(exists=True))
def local_cache_check(url: str, file_name: str | Path) -> BeautifulSoup:
    # url_hash = hash(url)
    # path = input('Please enter complete filepath to search: ')
    print('check')
    path = file_name
    file_list = os.listdir(f'{path}')
    file_path = os.path.join(path, file_name)
    if file_name in file_list:
        print('Retrieving the file from the directory')
        with open(file_path, 'r') as file:
            yelp_soup = file.read()
    else:
        print('Writing new file in the directory')
        yelp_page = requests.get(url)
        yelp_soup = BeautifulSoup(yelp_page.content, 'html.parser')
        with open(file_path, 'w') as file:
            file.write(yelp_soup)
    return yelp_soup






cli.add_command(url_generator)
cli.add_command(local_cache_check)

if __name__ == "__main__":
    cli()


