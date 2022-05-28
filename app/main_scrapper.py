# import libraries
import logging
import urllib.request
from bs4 import BeautifulSoup
from helpers import checkIfFolderExistsAndCreateIfNot, checkInternetConnection, checkIfUrlExists
from database import Database

# Set logging to info
logging.basicConfig(level = logging.INFO)

class GeneralImage:

    def __init__(self, name, container_link, image_link):
        self.name = name
        self.container_link = container_link
        self.image_link = image_link


def load_images_page(name, images_container_list):
    generalImage_list = []

    for container_url in images_container_list:
        try:
            with urllib.request.urlopen(container_url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                image_box = soup.find('img', attrs={'id': 'image'})
                logging.info(f'Loading Image: {image_box["src"]}')

                generalImage = GeneralImage(name, container_url, image_box['src'])
                generalImage_list.append(generalImage)
        except Exception as e:
            logging.error(f'Unable to load Image: {container_url}')

    return generalImage_list


def load_html_page(search):
    images_container_list = []
    with urllib.request.urlopen(search) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        image_box = soup.find('div', attrs={'class': 'thumbnail-container'})

        try:
            for a in image_box.find_all('a', href=True):
                images_container_list.append(a['href'])
        except:
            logging.error('No Images Found!')

    return images_container_list


def askForSearchInput():
    search = ''
    while search == '':
        search = input('Search: ')
    return search

if __name__ == "__main__":
   

    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        database_object = Database()

        if connection:

            search = ''
            search = askForSearchInput()
            search_url = f'https://gelbooru.com/index.php?page=post&s=list&tags={search}&pid=0'
            search_connection = checkIfUrlExists(search_url)
            if search_url != '' and search_connection and database_object.connection:
                
                images_container_list = load_html_page(search_url)
                generalImage_list = load_images_page(search, images_container_list)

                try:
                    if len(generalImage_list) > 0:
                        logging.info(f'{len(generalImage_list)} - Images Found!')
                        for generalImage in generalImage_list:
                            logging.info(f'Valid => {generalImage.name} : {generalImage.image_link}')

                        if database_object.connection:
                            logging.info('Saving images to database...')
                            database_object.insert_general_image_data(generalImage_list)
                            database_object.close_database()
                            logging.info('Done!')

                    else:
                        logging.error('No Images Found!')

                except ValueError as error:
                    logging.error('No Images Found!')
            else:
                logging.error('Please fill all the fields!')

        else:
            raise Exception("Sorry, unable to connect to the Internet!")

    except Exception as err:
        logging.error(err)
