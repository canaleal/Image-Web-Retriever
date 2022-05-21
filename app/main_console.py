# Created by: Alex Canales on May 21, 2022

import logging
from helpers import checkIfFolderExistsAndCreateIfNot, checkInternetConnection, downloadListOfImagesFromUrl, getListOfPostsThatHaveJPGorPNG, downloadListOfImagesFromUrl
from instance import createRedditObject
from service import getImageCollection

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


def askForPopularityFromValidArray(validArray):
    popularity = ''
    while popularity == '':
        popularity = input('Popularity [Hot, New, Top]: ')
        if popularity not in validArray:
            print('Please enter a valid option')
            popularity = ''
    return popularity


if __name__ == "__main__":
    try:
        connection = checkInternetConnection()
        checkIfFolderExistsAndCreateIfNot('app/output')
        reddit_object = createRedditObject()

        if reddit_object and connection:

            images = None
            search = ''
            count = 0
            topic = ''
            popularity = ''

            search = askForSearchInput()
            count = askForNumberOfPosts()
            topic = askForTopicFromValidArray(['Subreddit', 'User'])
            popularity = askForPopularityFromValidArray(['Hot', 'New', 'Top'])

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
