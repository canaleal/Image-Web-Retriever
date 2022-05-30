# Created by: Alex Canales on May 21, 2022

import logging
from utils.check_folder import checkIfFolderExistsAndCreateIfNot
from utils.check_internet import checkInternetConnection
from utils.download_image import getListOfPostsThatHaveJPGorPNG, downloadListOfImagesFromUrl
from utils.ask_input import askForSearchInput, askForRedditNumberOfPosts, askForRedditTopicFromValidArray, getRedditTopicValueInteger, askForRedditPopularityFromValidArray, getRedditPopularityValueInteger

from services.reddit_service import Reddit
from db.database import Database

# Set logging to info
logging.basicConfig(level = logging.INFO)


if __name__ == "__main__":
    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        reddit_object = Reddit()
        database_object = Database()

        if reddit_object and connection:

            images = None
            search = ''
            count = 0
            topic = ''
            popularity = ''

            search = askForSearchInput()
            count = askForRedditNumberOfPosts()
            topic = askForRedditTopicFromValidArray(['Subreddit', 'User'])
            topic_value = getRedditTopicValueInteger(topic)
            popularity = askForRedditPopularityFromValidArray(['Hot', 'New', 'Top'])
            popularity_value = getRedditPopularityValueInteger(popularity)

            if search != '' and count != 0 and topic != '' and popularity != '':

                images = reddit_object.getImageCollection(topic, search, count, popularity)
            
                try:
                    images = getListOfPostsThatHaveJPGorPNG(images)
                    if len(images) > 0:
                        logging.info(f'{len(images)} - Images Found!')
                        for image in images:
                            logging.info(f'Valid => {image} : {image.url}')

                        logging.info('Downloading images...')
                        checkIfFolderExistsAndCreateIfNot(f'app/output/{search}')
                        downloadListOfImagesFromUrl(search, images)
                        logging.info('Done!')
                        
                       
                        if database_object.connection:
                            logging.info('Saving images to database...')
                            database_object.insert_reddit_image_data(search, topic_value, popularity_value, images)
                            database_object.close_database()
                            logging.info('Done!')
                        
                    else:
                        logging.error('No Images Found!')

                except ValueError as error:
                    logging.error('No Images Found!')
            else:
                logging.error('Please fill all the fields!')

        else:
            raise Exception("Sorry, unable to connect to Reddit!")

    except Exception as err:
        logging.error(err)
