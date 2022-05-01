# Created by: Alex Canales on May 1, 2022

import logging
import requests
import os
from urllib.request import urlretrieve

def checkInternetConnection():
    try:
        requests.get('http://google.com')
        return True
    except:
        return False


def checkIfFolderExistsAndCreateIfNot(folderName):

    if not os.path.exists(folderName):
        os.makedirs(folderName)
        return False
    else:
        return True


def getListOfPostsThatHaveJPGorPNG(posts):
    listOfPosts = []
    print(posts)
    for post in posts:
        logging.error(post)
        try:
            if  post.url.endswith('.jpg') or post.url.endswith('.png'):
                listOfPosts.append(post)
        except AttributeError:
            pass        
        
    return listOfPosts


    
def downloadImageToFileGiveUrl(url, fileName):
    try:
        urlretrieve(url, fileName)
    except:
        pass

def downloadListOfImagesFromUrl(search, listOfImages):
    checkIfFolderExistsAndCreateIfNot(f'app/output/{search}')
    for image in listOfImages:
        downloadImageToFileGiveUrl(image.url, f'app/output/{search}/{image.id}.jpg')