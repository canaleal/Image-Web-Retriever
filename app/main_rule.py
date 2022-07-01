# import libraries
import logging
import time
import urllib.request
from bs4 import BeautifulSoup
from requests import request
import requests
from utils.check_folder import checkIfFolderExistsAndCreateIfNot
from utils.check_internet import checkInternetConnection, checkIfUrlExists

from utils.ask_input import askForSearchInput

from db.database import Database
from models.general_image import GeneralImage


import os
from dotenv import load_dotenv
load_dotenv()

# Set logging to info
logging.basicConfig(level = logging.INFO)


def load_images_page(name):
    generalImage_list = []


    try:
           
        url = os.getenv('RULE_API') + name
        headers = {'user-agent': 'my-app/0.0.1'}
        response = requests.get(url, headers=headers)
        response_json = response.json()
        
        for element in response_json:
            container_url = element['file_url']
            image_url = element['preview_url']
            logging.info(f'Loading Image: {container_url}')
           
        
            generalImage = GeneralImage(name, container_url, image_url)
            generalImage_list.append(generalImage)

    except Exception as e:
        logging.error(f'Unable to load Image: {container_url} => {e}')

    return generalImage_list


if __name__ == "__main__":
   

    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        database_object = Database()

        if connection:

            search = askForSearchInput()
            rule_url = os.getenv('RULE_URL')
            search_url = f'https://{rule_url}/index.php?page=post&s=list&tags={search}'
            search_connection = checkIfUrlExists(search_url)
            
            if search_url != '' and search_connection and database_object.connection:
               
                generalImage_list = load_images_page(search)

                try:
                    if len(generalImage_list) > 0:
                        logging.info(f'{len(generalImage_list)} - Images Found!')
                        for generalImage in generalImage_list:
                            logging.info(f'Valid => {generalImage.name} : {generalImage.container_link}')

                        if database_object.connection:
                            logging.info('Saving images to database...')
                            database_object.insert_rule_general_image_data(generalImage_list)
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
