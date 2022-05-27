# Created by: Alex Canales on May 21, 2022

from cmath import log
import logging
from helpers import checkIfFolderExistsAndCreateIfNot, checkInternetConnection, downloadListOfImagesFromUrl, getListOfPostsThatHaveJPGorPNG, downloadListOfImagesFromUrl
from instance import createRedditObject, getImageCollection
from database import Database

# Set logging to info
logging.basicConfig(level = logging.INFO)

def askForNumberOfPosts():
    count = 0
    while count == 0:
        try:
            count = int(input('How many posts for Images? '))
        except ValueError:
            print('Please enter a number')
    return count


def askForSearchInput():
    search = ''
    while search == '':
        search = input('Search: ')
    return search


def askForTopicFromValidArray(validArray):
    topic = ''
    while topic == '':
        topic = input('Topic [Subreddit, User]: ')
        if topic not in validArray:
            print('Please enter a valid option')
            topic = ''
    return topic

def getTopicValueInteger(topic):
    if topic == 'Subreddit':
        return 1
    elif topic == 'User':
        return 2


def askForPopularityFromValidArray(validArray):
    popularity = ''
    while popularity == '':
        popularity = input('Popularity [Hot, New, Top]: ')
        if popularity not in validArray:
            print('Please enter a valid option')
            popularity = ''
    return popularity

def getPopularityValueInteger(popularity):
    if popularity == 'Hot':
        return 1
    elif popularity == 'New':
        return 2
    elif popularity == 'Top':
        return 3

if __name__ == "__main__":
    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        reddit_object = createRedditObject()
        database_object = Database()

        if reddit_object and connection:

            images = None
            search = ''
            count = 0
            topic = ''
            popularity = ''

            search = askForSearchInput()
            count = askForNumberOfPosts()
            topic = askForTopicFromValidArray(['Subreddit', 'User'])
            topic_value = getTopicValueInteger(topic)
            popularity = askForPopularityFromValidArray(['Hot', 'New', 'Top'])
            popularity_value = getPopularityValueInteger(popularity)

            if search != '' and count != 0 and topic != '' and popularity != '':

                images = getImageCollection(topic, reddit_object, search, count, popularity)
            
                try:
                    images = getListOfPostsThatHaveJPGorPNG(images)
                    if len(images) > 0:
                        logging.info(f'{len(images)} - Images Found!')
                        for image in images:
                            logging.info(f'Valid => {image} : {image.url}')

                        logging.info('Downloading images...')
                        downloadListOfImagesFromUrl(search, images)
                        logging.info('Done!')
                        
                       
                        if database_object.connection:
                            logging.info('Saving images to database...')
                            database_object.insert_images_data(search, topic_value, popularity_value, images)
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
